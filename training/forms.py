from django import forms
from django.core.exceptions import ValidationError

from .models import TrainingSession, SessionExercise, ExerciseType


class TrainingSessionForm(forms.ModelForm):
    class Meta:
        model = TrainingSession
        fields = ["start", "end"]
        widgets = {
            "start": forms.DateTimeInput(
                attrs={"type": "datetime-local", "class": "form-control"}
            ),
            "end": forms.DateTimeInput(
                attrs={"type": "datetime-local", "class": "form-control"}
            ),
        }

    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get("start")
        end = cleaned_data.get("end")

        if start and end and end < start:
            raise ValidationError(
                {
                    "end": "Data zakończenia nie może być wcześniejsza niż data rozpoczęcia."
                }
            )

        return cleaned_data


class SessionExerciseForm(forms.ModelForm):
    class Meta:
        model = SessionExercise
        fields = ["training_session", "exercise_type", "weight", "sets", "reps"]
        widgets = {
            "training_session": forms.Select(attrs={"class": "form-select"}),
            "exercise_type": forms.Select(attrs={"class": "form-select"}),
            "weight": forms.NumberInput(attrs={"class": "form-control"}),
            "sets": forms.NumberInput(attrs={"class": "form-control"}),
            "reps": forms.NumberInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user")
        super().__init__(*args, **kwargs)
        self.fields["training_session"].queryset = (
            TrainingSession.objects.filter(created_by=user).order_by("-start")
        )

        self.fields["exercise_type"].queryset = ExerciseType.objects.order_by("name")


class ExerciseTypeForm(forms.ModelForm):
    class Meta:
        model = ExerciseType
        fields = ["name"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
        }
