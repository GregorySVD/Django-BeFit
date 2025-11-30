from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils import timezone

from .models import ExerciseType, TrainingSession, SessionExercise


def home(request):
    return render(request, "training/home.html")


# --- LISTY PODSTAWOWE ---


def exercise_type_list(request):
    """
    Publiczna lista typów ćwiczeń (bez logowania).
    """
    types = ExerciseType.objects.all().order_by("name")
    return render(request, "training/exercise_type_list.html", {"types": types})


@login_required
def training_session_list(request):
    """
    Lista sesji treningowych zalogowanego użytkownika.
    """
    sessions = (
        TrainingSession.objects.filter(created_by=request.user)
        .order_by("-start")
    )
    return render(request, "training/training_session_list.html", {"sessions": sessions})


@login_required
def session_exercise_list(request):
    """
    Lista wykonanych ćwiczeń zalogowanego użytkownika.
    """
    exercises = (
        SessionExercise.objects
        .filter(created_by=request.user)
        .select_related("exercise_type", "training_session")
        .order_by("-training_session__start")
    )
    return render(request, "training/session_exercise_list.html", {"exercises": exercises})

@login_required
def stats_view(request):
    """
    Prosty widok statystyk z ostatnich 4 tygodni (28 dni).
    Na razie tylko przekazujemy dane do szablonu,
    logikę agregacji zrobimy później.
    """
    since = timezone.now() - timedelta(days=28)

    exercises = (
        SessionExercise.objects
        .filter(created_by=request.user, training_session__start__gte=since)
        .select_related("exercise_type", "training_session")
    )
    return render(request, "training/stats.html", {"exercises": exercises, "since": since})
