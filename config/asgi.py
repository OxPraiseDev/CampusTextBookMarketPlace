import os

# 1. SET THE SETTINGS MODULE FIRST
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# 2. INITIALIZE DJANGO BEFORE IMPORTING MODELS
from django.core.asgi import get_asgi_application
django_asgi_app = get_asgi_application() # <--- This line is the magic fix

# 3. NOW IT IS SAFE TO IMPORT YOUR ROUTING (which uses models)
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import apps.interactions.routing

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(
        URLRouter(
            apps.interactions.routing.websocket_urlpatterns
        )
    ),
})