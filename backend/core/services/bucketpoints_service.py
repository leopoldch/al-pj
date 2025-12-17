from core.models import BucketPoint
from core.serializers import BucketPointSerializer
from django.contrib.auth.models import User
from core.websocket.utils import send_ws_message_to_user
from core.websocket.messages import WebSocketMessageType
from rest_framework.exceptions import ValidationError, NotFound

class BucketPointService:

    @staticmethod
    def get_all() -> list:
        bucket_points = BucketPoint.objects.all()
        serializer = BucketPointSerializer(bucket_points, many=True)
        data = list(serializer.data)
        data.sort(key=lambda x: x["created_at"], reverse=True)
        return data

    @classmethod
    def create(cls, data: dict, context: dict) -> dict:
        """Crée un bucket point et notifie tout le monde."""
        serializer = BucketPointSerializer(data=data, context=context)
        
        if not serializer.is_valid():
            raise ValidationError(serializer.errors)

        bucket = serializer.save()
        payload = BucketPointSerializer(bucket).data

        cls._broadcast_change(WebSocketMessageType.BUCKETPOINT_CREATED, {"data": payload})
        
        return payload

    @classmethod
    def update(cls, pk: int, data: dict) -> dict:
        try:
            bucket_point = BucketPoint.objects.get(pk=pk)
        except BucketPoint.DoesNotExist:
            raise NotFound("Bucket point not found.")

        serializer = BucketPointSerializer(bucket_point, data=data, partial=True)
        
        if not serializer.is_valid():
            raise ValidationError(serializer.errors)

        bucket = serializer.save()
        payload = BucketPointSerializer(bucket).data

        cls._broadcast_change(WebSocketMessageType.BUCKETPOINT_UPDATED, {"data": payload})

        return payload

    @classmethod
    def delete(cls, pk: int) -> None:
        try:
            bucket_point = BucketPoint.objects.get(pk=pk)
        except BucketPoint.DoesNotExist:
            raise NotFound("Bucket point not found.")

        payload_id = bucket_point.id
        bucket_point.delete()

        cls._broadcast_change(WebSocketMessageType.BUCKETPOINT_DELETED, {"id": payload_id})

    @staticmethod
    def _broadcast_change(message_type: str, message_data: dict):
        recipients = User.objects.all().values_list("id", flat=True)
        
        for uid in recipients:
            send_ws_message_to_user(uid, message_type, message_data)