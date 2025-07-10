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
from channels.generic.websocket import AsyncWebsocketConsumer


class WebSocketManager(AsyncWebsocketConsumer):
    async def connect(self):
        self.scope["user"] = await self.get_user()
        user = self.scope["user"]
        if not user.is_authenticated:
            await self.close()
        else:
            self.user_group_name = f"user_{user.id}"
            await self.channel_layer.group_add(self.user_group_name, self.channel_name)
            await self.accept()
            print(f"User {user} connected to group {self.user_group_name}")

    async def disconnect(self, close_code):
        if hasattr(self, "user_group_name"):
            await self.channel_layer.group_discard(
                self.user_group_name, self.channel_name
            )

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
        await self.send(text_data=json.dumps(event["payload"]))
