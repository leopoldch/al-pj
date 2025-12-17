from django.contrib.auth.models import User
from channels.layers import get_channel_layer

import redis
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

REDIS_URL = "redis://" + os.getenv("REDIS_HOST", "localhost")
r = redis.Redis.from_url(REDIS_URL)

class UserService:

    def getPresenceData(self, user_id):
        channel_layer = get_channel_layer()

        if channel_layer is None:
            raise Exception("WebSocket channel layer not available.")
        
        other_user = User.objects.exclude(id=user_id).first()
        
        if not other_user:
            raise Exception("No other user found.")

        is_online = r.sismember("online_users", str(other_user.id))
        return {
            "is_online": is_online,
            "name": other_user.get_full_name() or other_user.username,
            "user_id": other_user.id,
        }