"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# project/urls.py
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import HomeView
from django.views.generic import TemplateView
from django.views.decorators.cache import never_cache

# Serve React build
index_view = never_cache(TemplateView.as_view(template_name='index.html'))
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',HomeView.as_view(),name='home'),
    path('api/auth/', include('app.urls', namespace='app')),
    path('api/',include('tasks.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    re_path(r'^.*$', index_view),
    ]
