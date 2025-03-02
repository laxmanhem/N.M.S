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


class PacketConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("network_packets", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("network_packets", self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        await self.send(text_data=json.dumps({"message": data["message"]}))

    async def send_packet(self, event):
        packet_data = event["data"]
        await self.send(text_data=json.dumps(packet_data))
