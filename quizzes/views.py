from django.shortcuts import render

def home(request):
    return render(request, 'quizzes/home.html')

def quiz_create(request):
    return render(request, 'quizzes/create_quiz.html')

def quiz_take(request, quiz_id):
    # We'll add quiz loading logic later
    return render(request, 'quizzes/take_quiz.html')

def quiz_results(request, quiz_id):
    # We'll add quiz loading logic later
    return render(request, 'quizzes/quiz_results.html')

def member_profile(request, member_id):
    # We'll add member loading logic later
    return render(request, 'quizzes/profile.html')