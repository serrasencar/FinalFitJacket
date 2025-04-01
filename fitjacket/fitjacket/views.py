from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import ProfileUpdateForm
from django.contrib.auth.models import User
from .forms import RegistrationForm
from .models import UserProfile
from django.contrib import messages
def index(request):
    template_data = {}
    template_data['title'] = 'FitJacket'
    if request.user.is_authenticated:
        user = request.user
        profile = user.userprofile  # assumes OneToOneField to User

        context = {
            'template_data': template_data,
            'first_name': user.first_name,
            'skill_level': profile.skill_level,
            'goals': profile.goals,
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
            user = form.save() #uses django's default model to store username and password
            skill_level = form.cleaned_data.get('skill_level')
            goals = form.cleaned_data.get('goals')

            # Create the profile
            UserProfile.objects.create( #uses customized userprofile model otherwise
                user=user,
                skill_level=skill_level,
                goals=goals
            )

            messages.success(request, "Account created! You can now log in.")
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'auth/register.html', {'form': form})

# LOGIN VIEW
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')  # You can change this to your homepage or dashboard
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
        p_form = ProfileUpdateForm(request.POST, instance=profile)

        if p_form.is_valid():
            p_form.save()
            return redirect('index')  # or wherever you want to go after saving
    else:
        p_form = ProfileUpdateForm(instance=profile)

    return render(request, 'auth/edit_profile.html', {
        'p_form': p_form,
    })