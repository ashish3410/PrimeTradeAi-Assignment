"""
ASGI config for backend project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
settings_module = 'backend.deployement_settings' if os.environ.get('RENDER_EXTERNAL_HOSTNAME') else 'backend.settings'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module )

application = get_asgi_application()
