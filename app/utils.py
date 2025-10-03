# accounts/utils.py
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings

def send_activation_email(request, user):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    activation_path = reverse('accounts:activate')  # /api/auth/activate/
    domain = request.get_host()
    activation_url = f"{request.scheme}://{domain}{activation_path}?uid={uid}&token={token}"
    subject = "Activate your account"
    message = f"Click to activate: {activation_url}"
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
