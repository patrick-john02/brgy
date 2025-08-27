import os
import django
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import lgu_admin.routing 

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "barangay.settings")
django.setup() 

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(lgu_admin.routing.websocket_urlpatterns)
    ),
})
