"""
ASGI config for network_monitoring_system project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""


import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
import network_monitoring_system.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'network_monitoring_system.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": URLRouter(network_monitoring_system.routing.websocket_urlpatterns),
})
