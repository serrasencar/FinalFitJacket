from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.forms import AuthenticationForm
from .forms import ProfileUpdateForm, GOAL_CHOICES
from django.contrib.auth.models import User
from .forms import RegistrationForm
from .models import UserProfile
from django.contrib import messages

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
    template_data = {}
    template_data['title'] = 'FitJacket'

    if request.user.is_authenticated:
        user = request.user
        profile, created = UserProfile.objects.get_or_create(user=user)

        context = {
            'template_data': template_data,
            'first_name': user.first_name,
            'skill_level': profile.skill_level,
            'goals': [GOAL_CHOICES.get(goal, goal) for goal in profile.goals],
        }
        return render(request, 'index.html', context)
    
    else:
        return render(request, 'index.html', {'template_data': template_data})

def about(request):
     template_data = {}
     template_data['title'] = 'About'
     return render(request, 'about.html', {'template_data': template_data})

def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            skill_level=form.cleaned_data.get('skill_level'),
            goals=form.cleaned_data.get('goals')
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

