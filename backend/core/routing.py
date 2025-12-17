from django.urls import re_path
from core.websocket.consumers import WebSocketManager

websocket_urlpatterns = [
    re_path(r"ws/$", WebSocketManager.as_asgi()),
]
