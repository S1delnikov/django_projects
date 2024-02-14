from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta


class Task(models.Model):
    """Задача. Состоит из подзадач."""
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=False)
    deadline = models.DateTimeField(auto_now_add=False)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.text
    
    
class Subtask(models.Model):
    """Подзадача. Её описание, статус."""
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    text = models.TextField()
    status = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'subtasks'

    def __str__(self):
        return f"{self.text[:50]}..."