from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("create/", views.quiz_create, name="quiz_create"),
    path("add_question/", views.add_question, name="add_question"),
    path("remove_question/", views.remove_question, name="remove_question"),
    path("take/<int:quiz_id>/", views.quiz_take, name="quiz_take"),
    path("results/<int:quiz_id>/", views.quiz_results, name="quiz_results"),
    path("profile/", views.default_profile, name="default_profile"),  # Add this line
    path("profile/<int:member_id>/", views.member_profile, name="profile"),
]
