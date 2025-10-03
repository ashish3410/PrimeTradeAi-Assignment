from django.contrib import admin
from .models import CustomUser

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'email', 'is_active', 'is_staff']

# register the model with the admin class
admin.site.register(CustomUser, CustomUserAdmin)

# Register your models here.
