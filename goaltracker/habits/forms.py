from django import forms
from .models import Habit, HabitLog


class HabitForm(forms.ModelForm):
    class Meta:
        model = Habit
        fields = ['name', 'description']

class HabitLogForm(forms.ModelForm):
    class Meta:
        model = HabitLog
        fields = ['status']





