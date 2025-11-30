from django.conf import settings
from django.core.validators import (
    MinLengthValidator,
    MinValueValidator,
    MaxValueValidator,
)
from django.db import models
from django.core.exceptions import ValidationError


class ExerciseType(models.Model):
    name = models.CharField(
        max_length=100,
        validators=[MinLengthValidator(3)],
        verbose_name="Nazwa ćwiczenia",
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Typ ćwiczenia"
        verbose_name_plural = "Typy ćwiczeń"

    def __str__(self) -> str:
        return self.name


class TrainingSession(models.Model):
    start = models.DateTimeField(verbose_name="Początek sesji")
    end = models.DateTimeField(verbose_name="Koniec sesji")

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="training_sessions",
        verbose_name="Utworzone przez",
    )

    class Meta:
        ordering = ["-start"]
        verbose_name = "Sesja treningowa"
        verbose_name_plural = "Sesje treningowe"

    def __str__(self) -> str:
        return f"Sesja {self.start:%Y-%m-%d %H:%M} – {self.end:%H:%M}"

    def clean(self):
        # Prosta walidacja: koniec po początku
        if self.end <= self.start:
            raise ValidationError(
                {"end": "Czas zakończenia musi być późniejszy niż czas rozpoczęcia."}
            )


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
        verbose_name="Typ ćwiczenia",
    )

    weight = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(1000)],
        verbose_name="Ciężar [kg]",
    )

    sets = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(100)],
        verbose_name="Liczba serii",
    )

    reps = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(100)],
        verbose_name="Liczba powtórzeń w serii",
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="session_exercises",
        verbose_name="Utworzone przez",
    )

    class Meta:
        verbose_name = "Wykonane ćwiczenie"
        verbose_name_plural = "Wykonane ćwiczenia"

    def __str__(self) -> str:
        return f"{self.exercise_type} – {self.sets}x{self.reps} @ {self.weight} kg"
