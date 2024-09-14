from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .forms import QuizForm, QuestionFormSet, AnswerFormSet
from .models import Quiz, Question, Answer


def home(request):
    return render(request, "quizzes/home.html")


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


def quiz_take(request, quiz_id):
    # We'll add quiz loading logic later
    return render(request, "quizzes/take_quiz.html")


def quiz_results(request, quiz_id):
    # We'll add quiz loading logic later
    return render(request, "quizzes/quiz_results.html")


def default_profile(request):
    # For now, we'll just redirect to a default member_id
    # You can change this logic later when you implement user authentication
    return redirect("profile", member_id=1)


def member_profile(request, member_id):
    # We'll add member loading logic later
    return render(request, "quizzes/profile.html", {"member_id": member_id})
