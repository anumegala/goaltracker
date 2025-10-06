from django.db import models
from django.utils import timezone

class Habit(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class HabitLog(models.Model):
    STATUS_CHOICES = [
        ('done', 'Done'),
        ('not_done', 'Not Done'),
    ]

    habit = models.ForeignKey(Habit, on_delete=models.CASCADE, related_name='logs')
    date = models.DateField(default=timezone.now)
    status = models.CharField(max_length=8, choices=STATUS_CHOICES)

    class Meta:
        unique_together = ('habit', 'date')  # Avoid duplicate logs for same day

    def __str__(self):
        return f"{self.habit.name} - {self.date} - {self.status}"
