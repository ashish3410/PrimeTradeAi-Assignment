# accounts/urls.py
from django.urls import path
from .views import RegisterView, ActivateView, ProfileView,MyTokenObtainPairView

app_name = 'accounts'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
     path('login/',MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path('activate/', ActivateView.as_view(), name='activate'),
    path('profile/', ProfileView.as_view(), name='profile'),
]
