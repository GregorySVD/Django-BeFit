from django import forms
from .models import ExerciseType, TrainingSession, SessionExercise


class ExerciseTypeForm(forms.ModelForm):
    class Meta:
        model = ExerciseType
        fields = ["name"]
        labels = {
            "name": "Nazwa ćwiczenia",
        }


class TrainingSessionForm(forms.ModelForm):
    class Meta:
        model = TrainingSession
        fields = ["start", "end"]
        labels = {
            "start": "Data i czas rozpoczęcia",
            "end": "Data i czas zakończenia",
        }
        widgets = {
            "start": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "end": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }


class SessionExerciseForm(forms.ModelForm):
    class Meta:
        model = SessionExercise
        fields = ["training_session", "exercise_type", "weight", "sets", "reps"]
        labels = {
            "training_session": "Sesja treningowa",
            "exercise_type": "Typ ćwiczenia",
            "weight": "Ciężar (kg)",
            "sets": "Liczba serii",
            "reps": "Powtórzenia na serię",
        }
