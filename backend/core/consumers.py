from channels.generic.websocket import AsyncWebsocketConsumer
import json


class EchoConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def receive(self, data):
        data = json.loads(data)
        # process the message

    async def disconnect(self, close_code):
        pass
