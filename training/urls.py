from django.urls import path
from . import views

urlpatterns = [
    # Strona główna
    path("", views.home, name="home"),

    # Typy ćwiczeń
    path("exercise-types/", views.exercise_type_list, name="exercise_type_list"),
    path(
        "exercise-types/create/",
        views.exercise_type_create,
        name="exercise_type_create",
    ),
    path(
        "exercise-types/<int:pk>/edit/",
        views.exercise_type_edit,
        name="exercise_type_edit",
    ),
    path(
        "exercise-types/<int:pk>/delete/",
        views.exercise_type_delete,
        name="exercise_type_delete",
    ),

    # Sesje treningowe
    path("training-sessions/", views.training_session_list, name="training_session_list"),
    path(
        "training-sessions/create/",
        views.training_session_create,
        name="training_session_create",
    ),
    path(
        "training-sessions/<int:pk>/",
        views.training_session_detail,
        name="training_session_detail",
    ),
    path(
        "training-sessions/<int:pk>/edit/",
        views.training_session_edit,
        name="training_session_edit",
    ),
    path(
        "training-sessions/<int:pk>/delete/",
        views.training_session_delete,
        name="training_session_delete",
    ),

    # Wykonane ćwiczenia
    path(
        "session-exercises/",
        views.session_exercise_list,
        name="session_exercise_list",
    ),
    path(
        "session-exercises/create/",
        views.session_exercise_create,
        name="session_exercise_create",
    ),
    path(
        "session-exercises/<int:pk>/edit/",
        views.session_exercise_edit,
        name="session_exercise_edit",
    ),
    path(
        "session-exercises/<int:pk>/delete/",
        views.session_exercise_delete,
        name="session_exercise_delete",
    ),

    # Statystyki
    path("stats/", views.stats_view, name="stats"),
]
