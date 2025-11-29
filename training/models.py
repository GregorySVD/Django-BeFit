from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class ExerciseType(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="Nazwa ćwiczenia",
        help_text='Podaj nazwę ćwiczenia, np. "Wyciskanie leżąc", "Przysiad".',
    )

    def __str__(self) -> str:
        return self.name


class TrainingSession(models.Model):
    start = models.DateTimeField(
        verbose_name="Początek treningu",
        help_text="Wybierz dzień i godzinę rozpoczęcia sesji.",
    )
    end = models.DateTimeField(
        verbose_name="Koniec treningu",
        help_text="Wybierz dzień i godzinę zakończenia sesji.",
    )

    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="training_sessions",
        verbose_name="Użytkownik",
    )

    def __str__(self) -> str:
        return f"{self.start:%Y-%m-%d %H:%M} – {self.end:%H:%M} ({self.created_by.username})"


class SessionExercise(models.Model):
    training_session = models.ForeignKey(
        TrainingSession,
        on_delete=models.CASCADE,
        related_name="exercises",
        verbose_name="Sesja treningowa",
    )

    exercise_type = models.ForeignKey(
        ExerciseType,
        on_delete=models.CASCADE,
        related_name="session_exercises",
        verbose_name="Rodzaj ćwiczenia",
    )

    weight = models.FloatField(
        verbose_name="Ciężar (kg)",
        help_text="Użyty ciężar w kilogramach. Dla ćwiczeń bez obciążenia wpisz 0.",
        validators=[
            MinValueValidator(0.0),
            MaxValueValidator(1000.0),
        ],
        default=0.0,
    )

    sets = models.PositiveIntegerField(
        verbose_name="Serie",
        help_text="Liczba serii.",
        validators=[
            MinValueValidator(1),
            MaxValueValidator(100),
        ],
    )

    reps = models.PositiveIntegerField(
        verbose_name="Powtórzenia",
        help_text="Liczba powtórzeń w jednej serii.",
        validators=[
            MinValueValidator(1),
            MaxValueValidator(100),
        ],
    )

    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="session_exercises",
        verbose_name="Użytkownik",
    )

    def __str__(self) -> str:
        return f"{self.exercise_type} ({self.sets}x{self.reps} @ {self.weight} kg)"
