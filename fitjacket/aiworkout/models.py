from django.db import models
from django.contrib.auth.models import User

class Workout(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    workout_type = models.CharField(max_length=100)  # Exercise name
    sets = models.IntegerField(default=1)
    reps = models.IntegerField(default=0)
    rest = models.CharField(max_length=50, blank=True)  # "90 seconds"
    equipment = models.CharField(max_length=100, blank=True)
    date = models.DateField()

    def __str__(self):
        return f"{self.workout_type} - {self.reps} reps on {self.date}"


# aiworkout/models.py

class Badge(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='badges/')
    rule_type = models.CharField(max_length=100)  # e.g., 'pushup', 'bench_press'
    threshold = models.PositiveIntegerField()      # e.g., 30 reps


