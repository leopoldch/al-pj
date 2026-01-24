from channels.generic.websocket import AsyncWebsocketConsumer
import json
import asyncio
import logging
from channels.db import database_sync_to_async
from jwt import decode as jwt_decode, ExpiredSignatureError, InvalidTokenError
from django.contrib.auth.models import AnonymousUser, User
from django.conf import settings
from urllib.parse import parse_qs
from core.websocket.messages import WebSocketMessageType
import os
from dotenv import load_dotenv, find_dotenv
from redis.asyncio import Redis
from typing import Optional
from datetime import datetime

load_dotenv(find_dotenv())

# Configure structured logging
logger = logging.getLogger("websocket")
logger.setLevel(logging.DEBUG if settings.DEBUG else logging.INFO)

REDIS_URL = "redis://" + os.getenv("REDIS_HOST", "localhost")

# Configuration constants
HEARTBEAT_INTERVAL = 30  # seconds
HEARTBEAT_TIMEOUT = 10  # seconds to wait for pong response
MAX_MESSAGE_SIZE = 65536  # 64KB max message size
CONNECTION_TIMEOUT = 10  # seconds

_async_redis_client: Optional[Redis] = None


async def get_async_redis_client() -> Redis:
    """Get async Redis client lazily to avoid connection issues during import."""
    global _async_redis_client
    if _async_redis_client is None:
        _async_redis_client = Redis.from_url(REDIS_URL, decode_responses=True)
    return _async_redis_client


class WebSocketManager(AsyncWebsocketConsumer):
    """
    WebSocket consumer for real-time updates.

    Features:
    - JWT authentication via query parameter
    - Heartbeat/ping-pong for connection health monitoring
    - Structured logging
    - Graceful error handling
    - User presence tracking via Redis
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.heartbeat_task: Optional[asyncio.Task] = None
        self.user_group_name: Optional[str] = None
        self.last_pong: Optional[datetime] = None
        self.is_closing = False

    async def connect(self):
        """Handle WebSocket connection with authentication."""
        try:
            self.scope["user"] = await self.get_user()
            user = self.scope["user"]

            if not user.is_authenticated:
                logger.warning(
                    "Connection rejected: unauthenticated user",
                    extra={"client": self.scope.get("client", ["unknown"])[0]},
                )
                await self.close(code=4001)
                return

            self.user_group_name = f"user_{user.id}"

            # Add to user's personal group
            await self.channel_layer.group_add(self.user_group_name, self.channel_name)

            # Add to broadcast group for global events
            await self.channel_layer.group_add("broadcast", self.channel_name)

            # Mark user online in Redis
            await self.mark_user_online(user.id)

            # Accept the connection
            await self.accept()

            logger.info(
                f"User connected",
                extra={
                    "user_id": user.id,
                    "username": user.username,
                    "group": self.user_group_name,
                    "channel": self.channel_name[:20],
                },
            )

            # Start heartbeat task
            self.heartbeat_task = asyncio.create_task(self.heartbeat_loop())

            # Broadcast presence to other users
            await self.broadcast_presence(user, connected=True)

        except Exception as e:
            logger.error(f"Error during connection: {e}", exc_info=True)
            await self.close(code=4000)

    async def disconnect(self, close_code):
        """Handle WebSocket disconnection with cleanup."""
        self.is_closing = True
        user = self.scope.get("user")

        # Cancel heartbeat task
        if self.heartbeat_task and not self.heartbeat_task.done():
            self.heartbeat_task.cancel()
            try:
                await self.heartbeat_task
            except asyncio.CancelledError:
                logger.debug("Heartbeat task cancelled during disconnect")

        if not user or not user.is_authenticated:
            logger.debug(f"Anonymous user disconnected (code: {close_code})")
            return

        logger.info(
            f"User disconnected",
            extra={
                "user_id": user.id,
                "username": user.username,
                "close_code": close_code,
            },
        )

        # Mark user offline
        await self.mark_user_offline(user.id)

        # Remove from groups
        if self.user_group_name:
            try:
                await self.channel_layer.group_discard(
                    self.user_group_name, self.channel_name
                )
            except Exception as e:
                logger.error(f"Error removing from user group: {e}")

        try:
            await self.channel_layer.group_discard("broadcast", self.channel_name)
        except Exception as e:
            logger.error(f"Error removing from broadcast group: {e}")

        # Broadcast disconnect to other users
        await self.broadcast_presence(user, connected=False)

    async def heartbeat_loop(self):
        """Send periodic pings to detect dead connections."""
        try:
            while not self.is_closing:
                await asyncio.sleep(HEARTBEAT_INTERVAL)

                if self.is_closing:
                    break

                try:
                    # Send ping message
                    await self.send(
                        text_data=json.dumps(
                            {
                                "type": "PING",
                                "data": {"timestamp": datetime.utcnow().isoformat()},
                            }
                        )
                    )
                    logger.debug(
                        "Heartbeat ping sent",
                        extra={
                            "user_id": getattr(self.scope.get("user"), "id", "unknown")
                        },
                    )
                except Exception as e:
                    logger.warning(f"Failed to send heartbeat ping: {e}")
                    break

        except asyncio.CancelledError:
            logger.debug("Heartbeat loop cancelled")
        except Exception as e:
            logger.error(f"Heartbeat loop error: {e}", exc_info=True)

    @database_sync_to_async
    def get_user(self) -> User:
        """Extract and validate JWT token from query string."""
        try:
            query_string = self.scope["query_string"].decode()

            if "accessToken" not in query_string:
                logger.debug("No access token in query string")
                return AnonymousUser()

            parsed = parse_qs(query_string)
            token = parsed.get("accessToken", [None])[0]

            if not token:
                logger.debug("Empty access token")
                return AnonymousUser()

            # Decode and validate JWT
            decoded_data = jwt_decode(token, settings.SECRET_KEY, algorithms=["HS256"])

            user_id = decoded_data.get("user_id")
            if not user_id:
                logger.warning("JWT missing user_id claim")
                return AnonymousUser()

            user = User.objects.get(id=user_id)
            return user

        except ExpiredSignatureError:
            logger.info("JWT token expired")
            return AnonymousUser()
        except InvalidTokenError as e:
            logger.warning(f"Invalid JWT token: {e}")
            return AnonymousUser()
        except User.DoesNotExist:
            logger.warning(f"User from JWT does not exist")
            return AnonymousUser()
        except Exception as e:
            logger.error(f"Unexpected error during authentication: {e}", exc_info=True)
            return AnonymousUser()

    async def receive(self, text_data=None, bytes_data=None):
        """Handle incoming WebSocket messages."""
        if not self.scope["user"].is_authenticated:
            logger.warning("Received message from unauthenticated connection")
            return

        if text_data is None:
            return

        # Validate message size
        if len(text_data) > MAX_MESSAGE_SIZE:
            logger.warning(
                f"Message too large",
                extra={
                    "user_id": self.scope["user"].id,
                    "size": len(text_data),
                    "max_size": MAX_MESSAGE_SIZE,
                },
            )
            await self.send(
                text_data=json.dumps(
                    {"type": "ERROR", "data": {"message": "Message too large"}}
                )
            )
            return

        try:
            data = json.loads(text_data)
            message_type = data.get("type")

            # Handle PONG response for heartbeat
            if message_type == "PONG":
                self.last_pong = datetime.utcnow()
                logger.debug("Received PONG", extra={"user_id": self.scope["user"].id})
                return

            # Log other messages for debugging
            logger.debug(
                f"Received message",
                extra={"user_id": self.scope["user"].id, "type": message_type},
            )

        except json.JSONDecodeError:
            logger.warning(
                "Received invalid JSON", extra={"user_id": self.scope["user"].id}
            )
            await self.send(
                text_data=json.dumps(
                    {"type": "ERROR", "data": {"message": "Invalid JSON format"}}
                )
            )

    async def send_message(self, event):
        """Handler for channel layer messages - sends to WebSocket client."""
        try:
            payload = event.get("payload", {})
            await self.send(text_data=json.dumps(payload))
        except Exception as e:
            logger.error(
                f"Error sending message to client: {e}",
                extra={
                    "user_id": getattr(self.scope.get("user"), "id", "unknown"),
                    "event_type": event.get("payload", {}).get("type"),
                },
            )

    async def broadcast_presence(self, user: User, connected: bool):
        """Broadcast user presence status to all connected clients."""
        try:
            message_type = (
                WebSocketMessageType.USER_PRESENCE_CONNECTED
                if connected
                else WebSocketMessageType.USER_PRESENCE_DISCONNECTED
            )

            await self.channel_layer.group_send(
                "broadcast",
                {
                    "type": "send.message",
                    "payload": {
                        "type": message_type.value,
                        "data": {
                            "user_id": user.id,
                            "name": user.get_full_name() or user.username,
                        },
                    },
                },
            )
        except Exception as e:
            logger.error(f"Error broadcasting presence: {e}")

    async def mark_user_online(self, user_id: int):
        """Mark user as online in Redis."""
        try:
            redis_client = await get_async_redis_client()
            await redis_client.sadd("online_users", str(user_id))
            # Set expiry on the user's presence (auto-cleanup if server crashes)
            await redis_client.expire("online_users", 3600)  # 1 hour TTL
            logger.debug(f"User {user_id} marked online")
        except Exception as e:
            logger.error(f"Redis error (mark_user_online): {e}")

    async def mark_user_offline(self, user_id: int):
        """Mark user as offline in Redis."""
        try:
            redis_client = await get_async_redis_client()
            await redis_client.srem("online_users", str(user_id))
            logger.debug(f"User {user_id} marked offline")
        except Exception as e:
            logger.error(f"Redis error (mark_user_offline): {e}")
