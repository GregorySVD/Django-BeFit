from datetime import timedelta

from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import ExerciseTypeForm, TrainingSessionForm, SessionExerciseForm
from .models import ExerciseType, TrainingSession, SessionExercise


def is_admin(user):
    return user.is_authenticated and user.is_staff



def home(request):
    return render(request, "training/home.html")


def exercise_type_list(request):
    """
    Publiczna lista typów ćwiczeń (bez logowania).
    """
    types = ExerciseType.objects.all().order_by("name")
    return render(request, "training/exercise_type_list.html", {"types": types})


@user_passes_test(is_admin)
def exercise_type_create(request):
    if request.method == "POST":
        form = ExerciseTypeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("exercise_type_list")
    else:
        form = ExerciseTypeForm()

    return render(request, "training/exercise_type_form.html", {"form": form})


@user_passes_test(is_admin)
def exercise_type_edit(request, pk):
    exercise_type = get_object_or_404(ExerciseType, pk=pk)

    if request.method == "POST":
        form = ExerciseTypeForm(request.POST, instance=exercise_type)
        if form.is_valid():
            form.save()
            return redirect("exercise_type_list")
    else:
        form = ExerciseTypeForm(instance=exercise_type)

    return render(request, "training/exercise_type_form.html", {"form": form, "object": exercise_type})


@user_passes_test(is_admin)
def exercise_type_delete(request, pk):
    exercise_type = get_object_or_404(ExerciseType, pk=pk)

    if request.method == "POST":
        exercise_type.delete()
        return redirect("exercise_type_list")

    return render(request, "training/exercise_type_confirm_delete.html", {"object": exercise_type})


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
def training_session_detail(request, pk):
    """
    Szczegóły pojedynczej sesji użytkownika.
    """
    session = get_object_or_404(
        TrainingSession,
        pk=pk,
        created_by=request.user,
    )
    return render(request, "training/training_session_detail.html", {"session": session})


@login_required
def training_session_create(request):
    if request.method == "POST":
        form = TrainingSessionForm(request.POST)
        if form.is_valid():
            session = form.save(commit=False)
            session.created_by = request.user
            session.save()
            return redirect("training_session_list")
    else:
        form = TrainingSessionForm()

    return render(request, "training/training_session_form.html", {"form": form})


@login_required
def training_session_edit(request, pk):
    session = get_object_or_404(
        TrainingSession,
        pk=pk,
        created_by=request.user,
    )

    if request.method == "POST":
        form = TrainingSessionForm(request.POST, instance=session)
        if form.is_valid():
            form.save()
            return redirect("training_session_list")
    else:
        form = TrainingSessionForm(instance=session)

    return render(request, "training/training_session_form.html", {"form": form, "session": session})


@login_required
def training_session_delete(request, pk):
    session = get_object_or_404(
        TrainingSession,
        pk=pk,
        created_by=request.user,
    )

    if request.method == "POST":
        session.delete()
        return redirect("training_session_list")

    return render(request, "training/training_session_confirm_delete.html", {"session": session})

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
def session_exercise_detail(request, pk):
    exercise = get_object_or_404(
        SessionExercise.objects.select_related("exercise_type", "training_session"),
        pk=pk,
        created_by=request.user,
    )
    return render(request, "training/session_exercise_detail.html", {"exercise": exercise})


@login_required
def session_exercise_create(request):
    if request.method == "POST":
        form = SessionExerciseForm(request.POST)
        form.fields["training_session"].queryset = TrainingSession.objects.filter(created_by=request.user)

        if form.is_valid():
            exercise = form.save(commit=False)
            exercise.created_by = request.user
            exercise.save()
            return redirect("session_exercise_list")
    else:
        form = SessionExerciseForm()
        form.fields["training_session"].queryset = TrainingSession.objects.filter(created_by=request.user)

    return render(request, "training/session_exercise_form.html", {"form": form})


@login_required
def session_exercise_edit(request, pk):
    exercise = get_object_or_404(
        SessionExercise,
        pk=pk,
        created_by=request.user,
    )

    if request.method == "POST":
        form = SessionExerciseForm(request.POST, instance=exercise)
        form.fields["training_session"].queryset = TrainingSession.objects.filter(created_by=request.user)

        if form.is_valid():
            form.save()
            return redirect("session_exercise_list")
    else:
        form = SessionExerciseForm(instance=exercise)
        form.fields["training_session"].queryset = TrainingSession.objects.filter(created_by=request.user)

    return render(request, "training/session_exercise_form.html", {"form": form, "exercise": exercise})


@login_required
def session_exercise_delete(request, pk):
    exercise = get_object_or_404(
        SessionExercise,
        pk=pk,
        created_by=request.user,
    )

    if request.method == "POST":
        exercise.delete()
        return redirect("session_exercise_list")

    return render(request, "training/session_exercise_confirm_delete.html", {"exercise": exercise})


@login_required
def stats_view(request):
    """
    Na razie: zbieramy ćwiczenia z ostatnich 4 tygodni.
    W kolejnym kroku możemy dorobić agregację (liczba powtórzeń, średnie ciężary itd.).
    """
    since = timezone.now() - timedelta(days=28)

    exercises = (
        SessionExercise.objects
        .filter(created_by=request.user, training_session__start__gte=since)
        .select_related("exercise_type", "training_session")
    )
    return render(
        request,
        "training/stats.html",
        {
            "exercises": exercises,
            "since": since,
        },
    )
