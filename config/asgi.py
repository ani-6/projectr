import os
import django
from django.conf import settings

# Initialize Django first
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.core.asgi import get_asgi_application
from django.contrib.staticfiles.handlers import ASGIStaticFilesHandler
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import apps.chat.routing

# Get the standard Django ASGI app
django_asgi_app = get_asgi_application()

# Define the main application with ProtocolTypeRouter
application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(
        URLRouter(
            apps.chat.routing.websocket_urlpatterns
        )
    ),
})

# Wrap with ASGIStaticFilesHandler to serve static files when running with Daphne
# This ensures CSS/JS load correctly in development
if settings.DEBUG:
    application = ASGIStaticFilesHandler(application)