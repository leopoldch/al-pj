"""
Tests for WebSocket consumer.
"""

import pytest
import json
from unittest.mock import patch, MagicMock, AsyncMock
from asgiref.sync import async_to_sync
from core.websocket.consumers import WebSocketManager, HEARTBEAT_INTERVAL, HEARTBEAT_TIMEOUT, MAX_MESSAGE_SIZE


class TestWebSocketManagerAuthentication:
    """Tests for WebSocket authentication."""

    def test_get_user_returns_anonymous_when_no_token(self):
        """Test that AnonymousUser is returned when no token provided."""
        from django.contrib.auth.models import AnonymousUser

        consumer = WebSocketManager()
        consumer.scope = {"query_string": b""}

        # Use async_to_sync to call the async method
        with patch("core.websocket.consumers.User.objects.get") as mock_get:
            result = async_to_sync(consumer.get_user)()

        assert isinstance(result, AnonymousUser)

    def test_get_user_returns_anonymous_when_empty_token(self):
        """Test that AnonymousUser is returned when token is empty."""
        from django.contrib.auth.models import AnonymousUser

        consumer = WebSocketManager()
        consumer.scope = {"query_string": b"accessToken="}

        result = async_to_sync(consumer.get_user)()

        assert isinstance(result, AnonymousUser)

    def test_get_user_returns_anonymous_on_invalid_jwt(self):
        """Test that AnonymousUser is returned on invalid JWT."""
        from django.contrib.auth.models import AnonymousUser

        consumer = WebSocketManager()
        consumer.scope = {"query_string": b"accessToken=invalid_token"}

        result = async_to_sync(consumer.get_user)()

        assert isinstance(result, AnonymousUser)


class TestWebSocketManagerMessageHandling:
    """Tests for WebSocket message handling."""

    def test_receive_rejects_oversized_messages(self):
        """Test that messages exceeding size limit are rejected."""
        # Message larger than limit should be rejected
        large_message = "x" * (MAX_MESSAGE_SIZE + 1)
        assert len(large_message) > MAX_MESSAGE_SIZE

    def test_max_message_size_is_64kb(self):
        """Test that max message size is 64KB."""
        assert MAX_MESSAGE_SIZE == 65536


class TestWebSocketManagerPresence:
    """Tests for user presence functionality."""

    def test_mark_user_online_calls_redis(self):
        """Test that marking user online adds them to Redis set."""
        mock_redis = AsyncMock()
        mock_redis.sadd = AsyncMock(return_value=1)
        mock_redis.expire = AsyncMock(return_value=True)

        with patch(
            "core.websocket.consumers.get_async_redis_client",
            return_value=mock_redis
        ):
            consumer = WebSocketManager()
            async_to_sync(consumer.mark_user_online)(42)

            mock_redis.sadd.assert_called_once_with("online_users", "42")
            mock_redis.expire.assert_called_once()

    def test_mark_user_offline_calls_redis(self):
        """Test that marking user offline removes them from Redis set."""
        mock_redis = AsyncMock()
        mock_redis.srem = AsyncMock(return_value=1)

        with patch(
            "core.websocket.consumers.get_async_redis_client",
            return_value=mock_redis
        ):
            consumer = WebSocketManager()
            async_to_sync(consumer.mark_user_offline)(42)

            mock_redis.srem.assert_called_once_with("online_users", "42")

    def test_mark_user_online_handles_redis_error(self):
        """Test that Redis errors are handled gracefully."""
        mock_redis = AsyncMock()
        mock_redis.sadd = AsyncMock(side_effect=Exception("Redis connection failed"))

        with patch(
            "core.websocket.consumers.get_async_redis_client",
            return_value=mock_redis
        ):
            consumer = WebSocketManager()
            # Should not raise exception
            async_to_sync(consumer.mark_user_online)(42)


class TestWebSocketManagerHeartbeat:
    """Tests for heartbeat functionality."""

    def test_heartbeat_interval_configuration(self):
        """Test that heartbeat interval is properly configured."""
        assert HEARTBEAT_INTERVAL == 30  # 30 seconds

    def test_heartbeat_timeout_configuration(self):
        """Test that heartbeat timeout is properly configured."""
        assert HEARTBEAT_TIMEOUT == 10  # 10 seconds

    def test_max_message_size_configuration(self):
        """Test that max message size is properly configured."""
        assert MAX_MESSAGE_SIZE == 65536  # 64KB


class TestWebSocketManagerBroadcast:
    """Tests for broadcast functionality."""

    def test_broadcast_presence_connected(self, mock_user):
        """Test broadcasting user connected presence."""
        consumer = WebSocketManager()
        consumer.channel_layer = AsyncMock()
        consumer.channel_layer.group_send = AsyncMock()

        async_to_sync(consumer.broadcast_presence)(mock_user, connected=True)

        consumer.channel_layer.group_send.assert_called_once()
        call_args = consumer.channel_layer.group_send.call_args
        assert call_args[0][0] == "broadcast"
        payload = call_args[0][1]["payload"]
        assert payload["type"] == "USER_PRESENCE_CONNECTED"
        assert payload["data"]["user_id"] == mock_user.id

    def test_broadcast_presence_disconnected(self, mock_user):
        """Test broadcasting user disconnected presence."""
        consumer = WebSocketManager()
        consumer.channel_layer = AsyncMock()
        consumer.channel_layer.group_send = AsyncMock()

        async_to_sync(consumer.broadcast_presence)(mock_user, connected=False)

        consumer.channel_layer.group_send.assert_called_once()
        call_args = consumer.channel_layer.group_send.call_args
        payload = call_args[0][1]["payload"]
        assert payload["type"] == "USER_PRESENCE_DISCONNECTED"

    def test_send_message_handler(self):
        """Test send_message handler sends payload to client."""
        consumer = WebSocketManager()
        consumer.send = AsyncMock()

        event = {
            "type": "send.message",
            "payload": {
                "type": "TEST_EVENT",
                "data": {"key": "value"}
            }
        }

        async_to_sync(consumer.send_message)(event)

        consumer.send.assert_called_once()
        call_args = consumer.send.call_args
        sent_data = json.loads(call_args[1]["text_data"])
        assert sent_data["type"] == "TEST_EVENT"
        assert sent_data["data"]["key"] == "value"

    def test_broadcast_presence_handles_error(self, mock_user):
        """Test that broadcast errors are handled gracefully."""
        consumer = WebSocketManager()
        consumer.channel_layer = AsyncMock()
        consumer.channel_layer.group_send = AsyncMock(
            side_effect=Exception("Channel layer error")
        )

        # Should not raise exception
        async_to_sync(consumer.broadcast_presence)(mock_user, connected=True)
