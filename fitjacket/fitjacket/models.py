from django.db import models
from django.contrib.auth.models import User

class Workout(models.Model):
    """
    Represents a workout session logged by a user.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    exercise_type = models.CharField(max_length=100)
    duration = models.PositiveIntegerField(help_text="Duration in minutes")
    calories_burned = models.PositiveIntegerField()
    reps = models.PositiveIntegerField(null=True, blank=True)
    sets = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.exercise_type} on {self.date}"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    skill_level = models.CharField(max_length=20)
    goals = models.JSONField()  # Stores goals as a list (e.g. ["weight_loss", "endurance"])

    def __str__(self):
        return self.user.username
