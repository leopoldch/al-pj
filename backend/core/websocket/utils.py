from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from typing import Union
from enum import Enum


def send_ws_message_to_user(user_id: int, event_type: Union[str, Enum], data: dict):
    channel_layer = get_channel_layer()
    if not channel_layer:
        return

    async_send = async_to_sync(channel_layer.group_send)
    event = event_type.name if isinstance(event_type, Enum) else str(event_type)

    async_send(
        f"user_{user_id}",
        {
            "type": "send.message",
            "payload": {
                "type": event,
                "data": data,
            },
        },
    )


def broadcast_ws_message(user_ids: list[int], event_type: Union[str, Enum], data: dict):
    for uid in user_ids:
        send_ws_message_to_user(uid, event_type, data)
