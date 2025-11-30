from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class ExerciseType(models.Model):
    name = models.CharField("Nazwa ćwiczenia", max_length=100)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class TrainingSession(models.Model):
    start = models.DateTimeField("Data i czas rozpoczęcia")
    end = models.DateTimeField("Data i czas zakończenia")
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="training_sessions",
        verbose_name="Utworzono przez",
    )

    class Meta:
        ordering = ["-start"]

    def clean(self):
        super().clean()
        if self.end and self.start and self.end < self.start:
            raise ValidationError(
                {"end": "Data zakończenia nie może być wcześniejsza niż data rozpoczęcia."}
            )

    def __str__(self) -> str:
        return f"Sesja {self.start:%Y-%m-%d %H:%M} – {self.end:%H:%M}"


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
        "Ciężar [kg]",
        validators=[MinValueValidator(0), MaxValueValidator(1000)],
    )
    sets = models.IntegerField(
        "Serie",
        validators=[MinValueValidator(1), MaxValueValidator(100)],
    )
    reps = models.IntegerField(
        "Powtórzenia",
        validators=[MinValueValidator(1), MaxValueValidator(100)],
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="session_exercises",
        verbose_name="Utworzono przez",
    )

    class Meta:
        ordering = ["-training_session__start"]

    def __str__(self) -> str:
        return f"{self.exercise_type} – {self.weight} kg x {self.sets} x {self.reps}"
