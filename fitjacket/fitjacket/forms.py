from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile


SKILL_LEVEL_CHOICES = [
    ('beginner', 'Beginner'),
    ('intermediate', 'Intermediate'),
    ('advanced', 'Expert'),
]

GOAL_CHOICES = [
    ( 'strength',  'Strength'),
    ('cardio', 'Cardio'),
    ('stretching', 'Stretching'),
    ('plyometrics', 'Plyometrics'),
    ('strongman', 'Strongman'),
]
        
class ProfileUpdateForm(forms.ModelForm):
    skill_level = forms.ChoiceField(choices=SKILL_LEVEL_CHOICES)
    goals = forms.MultipleChoiceField(
        choices=GOAL_CHOICES,
        widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = UserProfile
        fields = ['skill_level', 'goals']

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    skill_level = forms.ChoiceField(choices=SKILL_LEVEL_CHOICES)
    goals = forms.MultipleChoiceField(
        choices=GOAL_CHOICES,
        widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'skill_level', 'goals']
