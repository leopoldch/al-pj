from django.contrib.auth.models import User
from core.serializers import MessageSerializer
from core.websocket.utils import send_ws_message_to_user
from core.websocket.messages import WebSocketMessageType
from core.utils import send_formatted_mail
from channels.layers import get_channel_layer
from ..models import Message
from rest_framework.exceptions import NotFound, ValidationError


class MessageService:

    @classmethod
    def create_message(cls, sender: User, data: dict, request_context=None) -> dict:
        serializer = MessageSerializer(data=data, context=request_context)
        if not serializer.is_valid():
            raise ValidationError(serializer.errors)
        serializer.save(user=sender)

        payload = serializer.data

        cls._notify_recipients(sender, payload, WebSocketMessageType.MESSAGE_CREATED)

        receiver = User.objects.exclude(id=sender.id).first()
        if receiver:
            try:
                send_formatted_mail(str(receiver.email), str(receiver.username))
            except Exception as e:
                print(f"Erreur d'envoi d'email: {e}")
        return payload

    @classmethod
    def _notify_recipients(cls, sender, message_payload, webSocketMessageType):
        channel_layer = get_channel_layer()
        if channel_layer is None:
            return
        recipients = User.objects.all().values_list("id", flat=True)

        for uid in recipients:

            send_ws_message_to_user(
                uid,
                webSocketMessageType,
                {
                    "message": message_payload,
                    "sender": {
                        "id": sender.id,
                        "username": sender.username,
                        "email": sender.email,
                    },
                },
            )

    @staticmethod
    def getAll():
        return Message.objects.all().order_by("-created_at")

    @classmethod
    def delete(cls, pk, user):
        try:
            message = Message.objects.get(pk=pk, user=user)
            if message.user != user:
                return False
            payload = MessageSerializer(message).data
            message.delete()
            cls._notify_recipients(user, payload, WebSocketMessageType.MESSAGE_DELETED)
            return True
        except Message.DoesNotExist:
            return False
