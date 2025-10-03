from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings

class Task(models.Model):
    PRIORITY = [('low','low'),('medium','medium'),('high','high')]
    STATUS = [('todo','todo'),('in_progress','in_progress'),('completed','completed')]
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS, default='todo')
    priority = models.CharField(max_length=10, choices=PRIORITY, default='medium')
    due_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
