from channels.generic.websocket import AsyncWebsocketConsumer
import json


# To mark a message as viewed by the other user :
# Verify that the user is authenticated
# Get the id of the message
# Verify that we are not making a self send message as viewed
# mark as viewed in db
# send to all the users through the websocket
# that the message has been viewed
# execpt the user who sent the message
from channels.db import database_sync_to_async
from rest_framework_simplejwt.tokens import UntypedToken
from jwt import decode as jwt_decode
from django.contrib.auth.models import AnonymousUser, User
from django.conf import settings
from urllib.parse import parse_qs


class WebSocketManager(AsyncWebsocketConsumer):
    async def connect(self):
        self.scope["user"] = await self.get_user()
        if not self.scope["user"].is_authenticated:
            await self.close()
        else:
            print(f"User {self.scope['user']} connected")
            await self.accept()

    @database_sync_to_async
    def get_user(self):
        try:
            token = parse_qs(self.scope["query_string"].decode())["accessToken"][0]
            decoded_data = jwt_decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user = User.objects.get(id=decoded_data["user_id"])
            return user
        except Exception as e:
            print("JWT Error:", e)
            return AnonymousUser()

    async def receive(self, data):
        # verify the user is authenticated
        data = json.loads(data)
        # process the message

    async def send_message(self, event):
        # send message to WebSocket
        await self.send(text_data=json.dumps(event))

    async def disconnect(self, close_code):
        pass
