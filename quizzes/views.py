from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
from .forms import QuizForm, QuestionFormSet, AnswerFormSet
from .models import Quiz, Question, Answer, QuizAttempt, UserAnswer, UserProfile, User
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Add this to the top of your views.py file
def handle_error(request, error_title, error_message):
    return render(
        request,
        "quizzes/error.html",
        {"error_title": error_title, "error_message": error_message},
    )


def home(request):
    all_quizzes = Quiz.objects.all().order_by("-created_at")
    paginator = Paginator(all_quizzes, 6)  # Show 6 quizzes per page
    page = request.GET.get("page")

    try:
        quizzes = paginator.page(page)
    except PageNotAnInteger:
        quizzes = paginator.page(1)
    except EmptyPage:
        quizzes = paginator.page(paginator.num_pages)

    return render(request, "quizzes/home.html", {"quizzes": quizzes})


@login_required
def quiz_create(request):
    if request.method == "POST":
        quiz_form = QuizForm(request.POST)
        question_formset = QuestionFormSet(request.POST, prefix="questions")
        if quiz_form.is_valid() and question_formset.is_valid():
            quiz = quiz_form.save(commit=False)
            quiz.creator = request.user
            quiz.save()

            questions = question_formset.save(commit=False)
            for question in questions:
                question.quiz = quiz
                question.save()
                answer_formset = AnswerFormSet(
                    request.POST, instance=question, prefix=f"answers_{question.id}"
                )
                if answer_formset.is_valid():
                    answer_formset.save()

            return redirect("quiz_detail", quiz_id=quiz.id)
    else:
        quiz_form = QuizForm()
        question_formset = QuestionFormSet(prefix="questions")

    context = {
        "quiz_form": quiz_form,
        "question_formset": question_formset,
    }
    return render(request, "quizzes/create_quiz.html", context)


@login_required
def add_question(request):
    form_index = int(request.GET.get("form_index", 0))
    question_form = QuestionFormSet(prefix="questions").empty_form
    answer_formset = AnswerFormSet(prefix=f"answers_{form_index}")
    return render(
        request,
        "quizzes/question_form.html",
        {
            "question_form": question_form,
            "answer_formset": answer_formset,
            "form_index": form_index,
        },
    )


@login_required
def remove_question(request):
    return HttpResponse("")  # This removes the question by returning an empty response


def quiz_detail(request, quiz_id):
    quiz = Quiz.objects.get(id=quiz_id)
    return render(request, "quizzes/quiz_detail.html", {"quiz": quiz})


# Update the quiz_take view
def quiz_take(request, quiz_id):
    try:
        quiz = get_object_or_404(Quiz, id=quiz_id)
        questions = quiz.questions.all().order_by("order")
        if not questions.exists():
            return handle_error(
                request, "Quiz Unavailable", "This quiz doesn't have any questions yet."
            )
        return render(
            request, "quizzes/take_quiz.html", {"quiz": quiz, "questions": questions}
        )
    except Http404:
        return handle_error(
            request, "Quiz Not Found", "The requested quiz does not exist."
        )


def quiz_results(request, quiz_id):
    try:
        quiz = get_object_or_404(Quiz, id=quiz_id)
        if request.method != "POST":
            return redirect("quiz_take", quiz_id=quiz_id)

        if request.method == "POST":
            score = 0
            total_questions = quiz.questions.count()

            quiz_attempt = QuizAttempt.objects.create(
                quiz=quiz,
                user=request.user if request.user.is_authenticated else None,
                started_at=timezone.now(),
            )

            user_answers = []

            for question in quiz.questions.all():
                answer_id = request.POST.get(f"question_{question.id}")
                if answer_id:
                    answer = Answer.objects.get(id=answer_id)
                    is_correct = answer.is_correct
                    if is_correct:
                        score += 1

                    user_answer = UserAnswer.objects.create(
                        quiz_attempt=quiz_attempt,
                        question=question,
                        answer=answer,
                        is_correct=is_correct,
                    )
                    user_answers.append(user_answer)

            quiz_attempt.score = score
            quiz_attempt.completed_at = timezone.now()
            quiz_attempt.save()

            return render(
                request,
                "quizzes/quiz_results.html",
                {
                    "quiz": quiz,
                    "score": score,
                    "total_questions": total_questions,
                    "user_answers": user_answers,
                    "quiz_attempt": quiz_attempt,
                },
            )

        return redirect("quiz_take", quiz_id=quiz_id)

    except Http404:
        return handle_error(
            request, "Quiz Not Found", "The requested quiz does not exist."
        )

    except Exception as e:
        return handle_error(request, "Error", f"An unexpected error occurred: {str(e)}")


def default_profile(request):
    # For now, we'll just redirect to a default member_id
    # You can change this logic later when you implement user authentication
    return redirect("profile", member_id=1)


# Update the member_profile view
def member_profile(request, member_id):
    try:
        user = get_object_or_404(User, id=member_id)
        profile, created = UserProfile.objects.get_or_create(user=user)
        quiz_attempts = QuizAttempt.objects.filter(user=user).order_by("-completed_at")
        created_quizzes = user.quiz_set.all().order_by("-created_at")

        context = {
            "profile": profile,
            "quiz_attempts": quiz_attempts,
            "created_quizzes": created_quizzes,
        }
        return render(request, "quizzes/profile.html", context)
    except Http404:
        return handle_error(
            request, "User Not Found", "The requested user profile does not exist."
        )
