# accounts/views.py
from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import RegisterSerializer, ProfileSerializer
# from .utils import send_activation_email
from django.contrib.auth import get_user_model
# from django.utils.http import urlsafe_base64_decode
# from django.contrib.auth.tokens import default_token_generator
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
# from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.db import transaction
from .serializers import RegisterSerializer
User = get_user_model()

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = "email"  # if you want email login; default is 'username'

    def validate(self, attrs):
        data = super().validate(attrs)
        # Include user info in response
        data.update({
            "user": {
                "id": self.user.id,

                "email": self.user.email,
            }
        })
        return data

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        with transaction.atomic():
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            
            # Save user but keep in transaction
            user = serializer.save()

            headers = self.get_success_headers(serializer.data)
            return Response(
                {"detail": "User created"},
                status=status.HTTP_201_CREATED,
                headers=headers
            )

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        serializer = ProfileSerializer(request.user)
        return Response(serializer.data)
    def patch(self, request):
        serializer = ProfileSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
