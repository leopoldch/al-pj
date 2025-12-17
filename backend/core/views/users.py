from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from ..serializers import (
    UserSerializer,
)
from django.contrib.auth.models import User
from channels.layers import get_channel_layer

import redis
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

REDIS_URL = "redis://" + os.getenv("REDIS_HOST", "localhost")
r = redis.Redis.from_url(REDIS_URL)

DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1", "t")

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not request.user or not request.user.is_authenticated:
            return Response(
                {"detail": "Authentication required."},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    




class PresenceIndicatorView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # verify is the other user has an active websocket connection
        if not request.user or not request.user.is_authenticated:
            return Response(
                {"detail": "Authentication required."},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        channel_layer = get_channel_layer()
        if channel_layer is None:
            return Response(
                {"detail": "WebSocket channel layer not available."},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )
        # Check if the other user has an active WebSocket connection
        other_user = User.objects.exclude(id=request.user.id).first()
        if not other_user:
            return Response(
                {"detail": "No other user found."}, status=status.HTTP_404_NOT_FOUND
            )
        is_online = r.sismember("online_users", str(other_user.id))
        return Response(
            {
                "is_online": is_online,
                "name": other_user.get_full_name() or other_user.username,
                "user_id": other_user.id,
            },
            status=status.HTTP_200_OK,
        )
