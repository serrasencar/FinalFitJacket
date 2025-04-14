from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.models import User

from .forms import RegistrationForm, ProfileUpdateForm, WorkoutForm
from .models import UserProfile, Workout

# Goal choices for home display
GOAL_CHOICES = {
    'strength': 'Strength',
    'cardio': 'Cardio',
    'stretching': 'Stretching',
    'plyometrics': 'Plyometrics',
    'powerlifting': 'Powerlifting',
    'strongman': 'Strongman',
}

def index(request):
    template_data = {'title': 'FitJacket'}

    if request.user.is_authenticated:
        user = request.user
        profile, _ = UserProfile.objects.get_or_create(user=user)

        context = {
            'template_data': template_data,
            'first_name': user.first_name,
            'skill_level': profile.skill_level,
            'goals': [GOAL_CHOICES.get(goal, goal) for goal in profile.goals],
        }
        return render(request, 'index.html', context)

    return render(request, 'index.html', {'template_data': template_data})

def about(request):
    return render(request, 'about.html', {'template_data': {'title': 'About'}})

def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(
                user=user,
                skill_level=form.cleaned_data.get('skill_level'),
                goals=form.cleaned_data.get('goals')
            )
            messages.success(request, "Account created! You can now log in.")
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'auth/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'auth/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('index')

@login_required
def edit_profile(request):
    profile = request.user.userprofile
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('index')
    else:
        form = ProfileUpdateForm(instance=profile)

    return render(request, 'auth/edit_profile.html', {'p_form': form})

@login_required
def log_workout(request):
    if request.method == 'POST':
        form = WorkoutForm(request.POST)
        if form.is_valid():
            workout = form.save(commit=False)
            workout.user = request.user
            workout.save()
            messages.success(request, "Workout logged successfully!")
            return redirect('workout_stats')
    else:
        form = WorkoutForm()
    return render(request, 'workouts/log_workout.html', {'form': form})

@login_required
def workout_stats(request):
    workouts = Workout.objects.filter(user=request.user).order_by('date')
    chart_data = [['Date', 'Calories Burned', 'Duration']]
    for w in workouts:
        chart_data.append([
            w.date.strftime('%Y-%m-%d'),
            w.calories_burned,
            w.duration
        ])
    return render(request, 'workouts/workout_stats.html', {
        'chart_data': chart_data
    })
