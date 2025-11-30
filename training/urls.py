from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("exercise-types/", views.exercise_type_list, name="exercise_type_list"),
    path("training-sessions/", views.training_session_list, name="training_session_list"),
    path("session-exercises/", views.session_exercise_list, name="session_exercise_list"),
    path("stats/", views.stats_view, name="stats"),
]
