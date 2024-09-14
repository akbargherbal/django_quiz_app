from django.contrib import admin
from .models import Quiz, Question, Answer, QuizAttempt, UserAnswer, UserProfile

admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(QuizAttempt)
admin.site.register(UserAnswer)
admin.site.register(UserProfile)