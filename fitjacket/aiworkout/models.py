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

    def __str__(self):
        return self.name
    
class UserBadge(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE)
    awarded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'badge')  # One badge per user

    def __str__(self):
        return f"{self.user.username} - {self.badge.name}"


