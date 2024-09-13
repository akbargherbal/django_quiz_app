from django.shortcuts import render, redirect


def home(request):
    return render(request, "quizzes/home.html")


def quiz_create(request):
    return render(request, "quizzes/create_quiz.html")


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
