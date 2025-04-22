from django.db.models import Count
from django.contrib.auth.models import User
from .models import Workout
from friends.models import Friendship
from datetime import date, timedelta
from django.db import models
from itertools import chain

def get_leaderboard_by_workouts_completed(user):
    friends = User.objects.filter(
        models.Q(friendship_user2__user1=user) | models.Q(friendship_user1__user2=user)
    ).distinct()

    leaderboard_users = list(chain(friends, User.objects.filter(id=user.id)))

    one_month_ago = date.today() - timedelta(days=30)
    leaderboard = (
        Workout.objects.filter(user__in=leaderboard_users, date__gte=one_month_ago)
        .values('user__username')
        .annotate(total_workouts=Count('id'))
        .order_by('-total_workouts')
    )
    leaderboard = leaderboard[:10]

    return leaderboard