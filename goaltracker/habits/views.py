import json
from datetime import timedelta
from django.utils import timezone
from django.shortcuts import render
from .models import Habit, HabitLog
from django.shortcuts import render, redirect
from .models import Habit
from .forms import HabitForm  # Make sure you have a form
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import Habit, HabitLog
from django.shortcuts import render, get_object_or_404, redirect
from .models import Habit
from .forms import HabitForm  # assuming you have a ModelForm for Habit
def mark_habit(request, habit_id):
    habit = get_object_or_404(Habit, id=habit_id)
    today = timezone.now().date()

    if request.method == "POST":
        HabitLog.objects.get_or_create(
            habit=habit,
            date=today,
            defaults={'status': 'done'}
        )
        return redirect('habit_list')

    return render(request, 'habits/mark_habit.html', {
        'habit': habit,
        'today': today
    })




def habit_list(request):
    habits = Habit.objects.all()
    today = timezone.now().date()
    logs = HabitLog.objects.filter(date=today)

    chart_data = []
    for habit in habits:
        dates = [(today - timedelta(days=i)) for i in range(6, -1, -1)]
        status_values = []
        for date in dates:
            log = HabitLog.objects.filter(habit=habit, date=date).first()
            status_values.append(1 if log and log.status == 'done' else 0)
        
        chart_data.append({
            'habit': habit.name,
            'dates': [d.strftime('%b %d') for d in dates],
            'values': status_values,
        })

    # Convert Python list → JSON string
    chart_data_json = json.dumps(chart_data)

    return render(request, 'habits/habit_list.html', {
        'habits': habits,
        'logs': logs,
        'today': today,
        'chart_data': chart_data_json
    })

def add_habit(request):
    if request.method == 'POST':
        form = HabitForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('habit_list')  # redirect to habit list page
    else:
        form = HabitForm()

    return render(request, 'habits/add_habit.html', {'form': form})



def edit_habit(request, habit_id):
    habit = get_object_or_404(Habit, id=habit_id)
    if request.method == 'POST':
        form = HabitForm(request.POST, instance=habit)
        if form.is_valid():
            form.save()
            return redirect('habit_list')
    else:
        form = HabitForm(instance=habit)
    return render(request, 'habits/edit_habit.html', {'form': form})


def delete_habit(request, habit_id):
    habit = get_object_or_404(Habit, id=habit_id)
    if request.method == 'POST':
        habit.delete()
        return redirect('habit_list')
    return render(request, 'delete_habit_confirm.html', {'habit': habit})

