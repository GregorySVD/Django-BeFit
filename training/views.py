from datetime import timedelta

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from .forms import TrainingSessionForm, SessionExerciseForm, ExerciseTypeForm
from .models import ExerciseType, TrainingSession, SessionExercise


# --- Strona główna ---


def home(request):
    return render(request, "training/home.html")


# --- Typy ćwiczeń ---


def exercise_type_list(request):
    """
    Publiczna lista typów ćwiczeń (bez logowania).
    """
    types = ExerciseType.objects.all().order_by("name")
    return render(request, "training/exercise_type_list.html", {"types": types})


@staff_member_required
def exercise_type_create(request):
    """
    Tworzenie typu ćwiczenia – tylko admin (is_staff).
    """
    if request.method == "POST":
        form = ExerciseTypeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("exercise_type_list")
    else:
        form = ExerciseTypeForm()

    return render(
        request,
        "training/exercise_type_form.html",
        {"form": form, "title": "Dodaj typ ćwiczenia"},
    )


@staff_member_required
def exercise_type_edit(request, pk):
    """
    Edycja typu ćwiczenia – tylko admin.
    """
    etype = get_object_or_404(ExerciseType, pk=pk)

    if request.method == "POST":
        form = ExerciseTypeForm(request.POST, instance=etype)
        if form.is_valid():
            form.save()
            return redirect("exercise_type_list")
    else:
        form = ExerciseTypeForm(instance=etype)

    return render(
        request,
        "training/exercise_type_form.html",
        {"form": form, "title": "Edytuj typ ćwiczenia"},
    )


@staff_member_required
def exercise_type_delete(request, pk):
    """
    Usuwanie typu ćwiczenia – tylko admin.
    """
    etype = get_object_or_404(ExerciseType, pk=pk)

    if request.method == "POST":
        etype.delete()
        return redirect("exercise_type_list")

    return render(
        request,
        "training/exercise_type_confirm_delete.html",
        {"type": etype},
    )


# --- Sesje treningowe ---


@login_required
def training_session_list(request):
    """
    Lista sesji treningowych zalogowanego użytkownika.
    """
    sessions = TrainingSession.objects.filter(created_by=request.user).order_by(
        "-start"
    )
    return render(
        request,
        "training/training_session_list.html",
        {"sessions": sessions},
    )


@login_required
def training_session_detail(request, pk):
    """
    Szczegóły pojedynczej sesji zalogowanego użytkownika
    + lista wykonanych ćwiczeń w tej sesji (tylko jego).
    """
    session = get_object_or_404(TrainingSession, pk=pk, created_by=request.user)
    exercises = (
        SessionExercise.objects.filter(
            training_session=session, created_by=request.user
        ).select_related("exercise_type")
    )
    context = {
        "session": session,
        "exercises": exercises,
    }
    return render(request, "training/training_session_detail.html", context)


@login_required
def training_session_create(request):
    """
    Tworzenie nowej sesji – przypisywana automatycznie do zalogowanego użytkownika.
    """
    if request.method == "POST":
        form = TrainingSessionForm(request.POST)
        if form.is_valid():
            session = form.save(commit=False)
            session.created_by = request.user
            session.save()
            return redirect("training_session_list")
    else:
        form = TrainingSessionForm()

    return render(
        request,
        "training/training_session_form.html",
        {"form": form, "title": "Dodaj sesję treningową"},
    )


@login_required
def training_session_edit(request, pk):
    """
    Edycja sesji – tylko jeśli należy do zalogowanego użytkownika.
    """
    session = get_object_or_404(TrainingSession, pk=pk, created_by=request.user)

    if request.method == "POST":
        form = TrainingSessionForm(request.POST, instance=session)
        if form.is_valid():
            form.save()
            return redirect("training_session_list")
    else:
        form = TrainingSessionForm(instance=session)

    return render(
        request,
        "training/training_session_form.html",
        {"form": form, "title": "Edytuj sesję treningową"},
    )


@login_required
def training_session_delete(request, pk):
    """
    Usuwanie sesji – tylko jeśli należy do zalogowanego użytkownika.
    """
    session = get_object_or_404(TrainingSession, pk=pk, created_by=request.user)

    if request.method == "POST":
        session.delete()
        return redirect("training_session_list")

    return render(
        request,
        "training/training_session_confirm_delete.html",
        {"session": session},
    )


# --- Wykonane ćwiczenia ---


@login_required
def session_exercise_list(request):
    """
    Lista wykonanych ćwiczeń zalogowanego użytkownika.
    """
    exercises = (
        SessionExercise.objects.filter(created_by=request.user)
        .select_related("exercise_type", "training_session")
        .order_by("-training_session__start")
    )
    return render(
        request,
        "training/session_exercise_list.html",
        {"exercises": exercises},
    )


@login_required
def session_exercise_create(request):
    if request.method == "POST":
        form = SessionExerciseForm(request.POST, user=request.user)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.created_by = request.user
            obj.save()
            return redirect("session_exercise_list")
    else:
        form = SessionExerciseForm(user=request.user)

    return render(
        request,
        "training/session_exercise_form.html",
        {"form": form, "title": "Dodaj ćwiczenie"},
    )


@login_required
def session_exercise_edit(request, pk):
    exercise = get_object_or_404(SessionExercise, pk=pk, created_by=request.user)

    if request.method == "POST":
        form = SessionExerciseForm(
            request.POST, instance=exercise, user=request.user
        )
        if form.is_valid():
            form.save()
            return redirect("session_exercise_list")
    else:
        form = SessionExerciseForm(instance=exercise, user=request.user)

    return render(
        request,
        "training/session_exercise_form.html",
        {"form": form, "title": "Edytuj ćwiczenie"},
    )


@login_required
def session_exercise_delete(request, pk):
    exercise = get_object_or_404(SessionExercise, pk=pk, created_by=request.user)

    if request.method == "POST":
        exercise.delete()
        return redirect("session_exercise_list")

    return render(
        request,
        "training/session_exercise_confirm_delete.html",
        {"exercise": exercise},
    )


# --- Statystyki ---


@login_required
def stats_view(request):
    """
    Widok statystyk z ostatnich 4 tygodni (28 dni).
    Na razie przekazujemy surowe dane, agregację można rozbudować.
    """
    since = timezone.now() - timedelta(days=28)

    exercises = (
        SessionExercise.objects.filter(
            created_by=request.user, training_session__start__gte=since
        ).select_related("exercise_type", "training_session")
    )

    return render(
        request,
        "training/stats.html",
        {
            "exercises": exercises,
            "since": since,
        },
    )
