# accounts/views.py
from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import RegisterSerializer, ProfileSerializer
from .utils import send_activation_email
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
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

            try:
                send_activation_email(self.request, user)  # your custom mail function
            except Exception as e:
                # Rollback user if email fails
                transaction.set_rollback(True)
                return Response(
                    {"detail": f"Failed to send activation email: {str(e)}"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

            headers = self.get_success_headers(serializer.data)
            return Response(
                {"detail": "User created. Check your email to activate."},
                status=status.HTTP_201_CREATED,
                headers=headers
            )

    
class ActivateView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        uidb64 = request.query_params.get('uid')
        token = request.query_params.get('token')
        if not uidb64 or not token:
            return Response({"detail":"Missing params"}, status=400)
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except Exception:
            return Response({"detail":"Invalid uid"}, status=400)
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            refresh = RefreshToken.for_user(user)
            return Response({"detail":"Activated","access":str(refresh.access_token),"refresh":str(refresh)}, status=200)
        return Response({"detail":"Invalid/expired token"}, status=400)

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
