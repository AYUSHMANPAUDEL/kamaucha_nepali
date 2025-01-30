import os
import django

# Ensure Django initializes before anything else
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kamaucha_nepali.settings')
django.setup()

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
import home.routing
from channels.auth import AuthMiddlewareStack

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': AuthMiddlewareStack(URLRouter(home.routing.websocket_urlpatterns)),
})
