from django.contrib import admin
from .models import Task

class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'priority', 'owner']

# register model with custom admin
admin.site.register(Task, TaskAdmin)
