from django.shortcuts import render

def home(request):
    return render(request, 'quizzes/home.html')

def quiz_create(request):
    return render(request, 'quizzes/quiz_create.html')

def quiz_take(request, quiz_id):
    # We'll add quiz loading logic later
    return render(request, 'quizzes/quiz_take.html')