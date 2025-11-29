from django.contrib import admin
from .models import ExerciseType, TrainingSession, SessionExercise


@admin.register(ExerciseType)
class ExerciseTypeAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(TrainingSession)
class TrainingSessionAdmin(admin.ModelAdmin):
    list_display = ("start", "end", "created_by")
    list_filter = ("created_by", "start")
    search_fields = ("created_by__username",)


@admin.register(SessionExercise)
class SessionExerciseAdmin(admin.ModelAdmin):
    list_display = ("exercise_type", "training_session", "weight", "sets", "reps", "created_by")
    list_filter = ("exercise_type", "created_by")
    search_fields = ("exercise_type__name", "created_by__username")
