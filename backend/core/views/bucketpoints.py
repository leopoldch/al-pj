from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from ..models import BucketPoint
from ..serializers import (
    BucketPointSerializer,
)
from django.contrib.auth.models import User
from channels.layers import get_channel_layer
from core.websocket.utils import send_ws_message_to_user
from core.websocket.messages import WebSocketMessageType
import redis
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

REDIS_URL = "redis://" + os.getenv("REDIS_HOST", "localhost")
r = redis.Redis.from_url(REDIS_URL)

DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1", "t")

class BucketPointView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not request.user or not request.user.is_authenticated:
            return Response(
                {"detail": "Authentication required."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        bucket_points = BucketPoint.objects.all()
        serializer = BucketPointSerializer(bucket_points, many=True)
        # sort the bucket points by created_at in descending order
        serializer.data.sort(key=lambda x: x["created_at"], reverse=True)
        return Response(serializer.data)

    def post(self, request):
        if not request.user or not request.user.is_authenticated:
            return Response(
                {"detail": "Authentication required."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        serializer = BucketPointSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            bucket = serializer.save()
            # FIXME: this is only temporary and works because this app is only
            # meant to be used by two users
            # in a real world scenario, we would need to filter the users based on the
            # conversation or group the message belongs to

            recipients = User.objects.all().values_list("id", flat=True)
            payload = BucketPointSerializer(bucket).data

            for uid in recipients:
                send_ws_message_to_user(
                    uid,
                    WebSocketMessageType.BUCKETPOINT_CREATED,
                    {"data": payload},
                )

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        if not request.user or not request.user.is_authenticated:
            return Response(
                {"detail": "Authentication required."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        try:
            bucket_point = BucketPoint.objects.get(pk=pk)
            payload = BucketPointSerializer(bucket_point).data
            bucket_point.delete()
            channel_layer = get_channel_layer()
            if channel_layer is not None:
                recipients = User.objects.all().values_list("id", flat=True)
                for uid in recipients:
                    send_ws_message_to_user(
                        uid,
                        WebSocketMessageType.BUCKETPOINT_DELETED,
                        {
                            "id": payload["id"],
                        },
                    )

            return Response(status=status.HTTP_204_NO_CONTENT)
        except BucketPoint.DoesNotExist:
            return Response(
                {"detail": "Bucket point not found."}, status=status.HTTP_404_NOT_FOUND
            )

    def put(self, request, pk):
        if not request.user or not request.user.is_authenticated:
            return Response(
                {"detail": "Authentication required."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        try:
            bucket_point = BucketPoint.objects.get(pk=pk)
            serializer = BucketPointSerializer(
                bucket_point, data=request.data, partial=True
            )
            if serializer.is_valid():
                bucket = serializer.save()
                # Notify other users about the update with websocket
                payload = BucketPointSerializer(bucket).data
                channel_layer = get_channel_layer()
                if channel_layer is not None:
                    recipients = User.objects.all().values_list("id", flat=True)
                    for uid in recipients:
                        send_ws_message_to_user(
                            uid,
                            WebSocketMessageType.BUCKETPOINT_UPDATED,
                            {"data": payload},
                        )
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except BucketPoint.DoesNotExist:
            return Response(
                {"detail": "Bucket point not found."}, status=status.HTTP_404_NOT_FOUND
            )
