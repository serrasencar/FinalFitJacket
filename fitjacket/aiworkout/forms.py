from django import forms
from .models import Workout

class WorkoutForm(forms.ModelForm):
    class Meta:
        model = Workout
        fields = ['workout_type', 'sets', 'reps', 'rest', 'equipment', 'date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

