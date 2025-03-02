from django.urls import path
from django.urls import re_path
from monitoring.consumers import PacketConsumer

websocket_urlpatterns = [
    path('ws/monitoring/', MonitoringConsumer.as_asgi()),

    re_path(r'ws/packets/$', PacketConsumer.as_asgi()),

]
