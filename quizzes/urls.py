from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('create/', views.quiz_create, name='quiz_create'),
    path('take/<int:quiz_id>/', views.quiz_take, name='quiz_take'),
    path('results/<int:quiz_id>/', views.quiz_results, name='quiz_results'),
    path('profile/<int:member_id>/', views.member_profile, name='member_profile'),
]