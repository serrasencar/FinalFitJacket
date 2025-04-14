from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Workout  # Adjust this if your Workout model is in another app

@login_required
def workout_stats(request):
    """
    Renders a line chart of calories burned and duration over time using Google Charts.
    """
    workouts = Workout.objects.filter(user=request.user).order_by('date')

    # Data format required by Google Charts
    data = [
        ['Date', 'Calories Burned', 'Duration']
    ]
    for workout in workouts:
        data.append([
            workout.date.strftime("%Y-%m-%d"),
            workout.calories_burned,
            workout.duration
        ])

    return render(request, 'workouts/workout_stats.html', {
        'chart_data': data
    })
