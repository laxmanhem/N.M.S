import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import NetworkLog

class MonitoringConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def receive(self, text_data):
        logs = NetworkLog.objects.order_by('-timestamp')[:10].values()
        await self.send(text_data=json.dumps({"logs": list(logs)}))

    async def disconnect(self, close_code):
        pass
