from channels.generic.websocket import AsyncWebsocketConsumer
import json

from channels.db import database_sync_to_async
from rest_framework_simplejwt.tokens import UntypedToken
from jwt import decode as jwt_decode
from django.contrib.auth.models import AnonymousUser, User
from django.conf import settings
from urllib.parse import parse_qs
from channels.generic.websocket import AsyncWebsocketConsumer
from core.websocket.messages import WebSocketMessageType

import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

from redis.asyncio import Redis

REDIS_URL = "redis://" + os.getenv("REDIS_HOST", "localhost")
redis_client = Redis.from_url(REDIS_URL)

# PLEASE NOTE THAT THIS IS A VERY BASIC IMPLEMENTATION
# WHICH IS MEANT TO BE USED ONLY BY 2 USERS
# THIS IS NOT MEANT TO BE USED FOR A GROUP CHAT

class WebSocketManager(AsyncWebsocketConsumer):
    async def connect(self):
        self.scope["user"] = await self.get_user()
        user = self.scope["user"]
        if not user.is_authenticated:
            await self.close()
        else:
            self.user_group_name = f"user_{user.id}"
            await self.channel_layer.group_add(self.user_group_name, self.channel_name)
            await self.mark_user_online(user.id)
            await self.accept()
            print(f"User {user} connected to group {self.user_group_name}")
            await self.channel_layer.group_send(
                "broadcast",
                {
                    "type": "send.message",
                    "payload": {
                        "type": WebSocketMessageType.USER_PRESENCE_CONNECTED,
                        "data": {
                            "user_id": user.id,
                            "name": user.get_full_name() or user.username,
                        },
                    },
                },
            )

    async def disconnect(self, close_code):
        print(f"User {self.scope['user']} disconnected")
        self.scope["user"] = await self.get_user()
        user = self.scope["user"]
        await self.mark_user_offline(user.id)
        if hasattr(self, "user_group_name"):
            await self.channel_layer.group_discard(
                self.user_group_name, self.channel_name
            )

        username = ""
        try:
            username = user.get_full_name()
        except Exception as e:
            username = user.username

        await self.channel_layer.group_send(
            "broadcast",
            {
                "type": "send.message",
                "payload": {
                    "type": WebSocketMessageType.USER_PRESENCE_DISCONNECTED,
                    "data": {
                        "user_id": user.id,
                        "name": username,
                    },
                },
            },
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

    async def mark_user_online(self, user_id: int):
        await redis_client.sadd("online_users", str(user_id))

    async def mark_user_offline(self, user_id: int):
        await redis_client.srem("online_users", str(user_id))
