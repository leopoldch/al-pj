"""
Tests for WebSocket utility functions.
"""

from unittest.mock import patch, MagicMock
from core.websocket.utils import send_ws_message_to_user, broadcast_ws_message
from core.websocket.messages import WebSocketMessageType


class TestSendWsMessageToUser:
    """Tests for send_ws_message_to_user function."""

    def test_sends_message_to_correct_user_group(self):
        """Test that message is sent to the correct user group."""
        mock_channel_layer = MagicMock()
        mock_async_send = MagicMock()
        mock_channel_layer.group_send = mock_async_send

        with patch(
            "core.websocket.utils.get_channel_layer", return_value=mock_channel_layer
        ):
            with patch(
                "core.websocket.utils.async_to_sync", return_value=mock_async_send
            ):
                user_id = 42
                event_type = WebSocketMessageType.BUCKETPOINT_CREATED
                data = {"id": 1, "title": "Test"}

                send_ws_message_to_user(user_id, event_type, data)

                mock_async_send.assert_called_once()
                call_args = mock_async_send.call_args
                assert call_args[0][0] == f"user_{user_id}"

    def test_message_payload_structure(self):
        """Test that message payload has correct structure."""
        mock_channel_layer = MagicMock()
        mock_async_send = MagicMock()

        with patch(
            "core.websocket.utils.get_channel_layer", return_value=mock_channel_layer
        ):
            with patch(
                "core.websocket.utils.async_to_sync", return_value=mock_async_send
            ):
                user_id = 1
                event_type = WebSocketMessageType.PHOTO_UPLOADED
                data = {"photo_id": 123}

                send_ws_message_to_user(user_id, event_type, data)

                call_args = mock_async_send.call_args
                message = call_args[0][1]

                assert message["type"] == "send.message"
                assert "payload" in message
                assert message["payload"]["type"] == "PHOTO_UPLOADED"
                assert message["payload"]["data"] == data

    def test_handles_enum_event_type(self):
        """Test that enum event types are properly converted."""
        mock_channel_layer = MagicMock()
        mock_async_send = MagicMock()

        with patch(
            "core.websocket.utils.get_channel_layer", return_value=mock_channel_layer
        ):
            with patch(
                "core.websocket.utils.async_to_sync", return_value=mock_async_send
            ):
                send_ws_message_to_user(1, WebSocketMessageType.MESSAGE_CREATED, {})

                call_args = mock_async_send.call_args
                payload = call_args[0][1]["payload"]
                assert payload["type"] == "MESSAGE_CREATED"

    def test_handles_string_event_type(self):
        """Test that string event types are passed through."""
        mock_channel_layer = MagicMock()
        mock_async_send = MagicMock()

        with patch(
            "core.websocket.utils.get_channel_layer", return_value=mock_channel_layer
        ):
            with patch(
                "core.websocket.utils.async_to_sync", return_value=mock_async_send
            ):
                send_ws_message_to_user(1, "CUSTOM_EVENT", {"key": "value"})

                call_args = mock_async_send.call_args
                payload = call_args[0][1]["payload"]
                assert payload["type"] == "CUSTOM_EVENT"

    def test_no_error_when_channel_layer_is_none(self):
        """Test that function handles missing channel layer gracefully."""
        with patch("core.websocket.utils.get_channel_layer", return_value=None):
            # Should not raise an exception
            send_ws_message_to_user(1, WebSocketMessageType.MESSAGE_CREATED, {})


class TestBroadcastWsMessage:
    """Tests for broadcast_ws_message function."""

    def test_broadcasts_to_all_users(self):
        """Test that message is broadcast to all specified users."""
        mock_channel_layer = MagicMock()
        mock_async_send = MagicMock()

        with patch(
            "core.websocket.utils.get_channel_layer", return_value=mock_channel_layer
        ):
            with patch(
                "core.websocket.utils.async_to_sync", return_value=mock_async_send
            ):
                user_ids = [1, 2, 3]
                event_type = WebSocketMessageType.BUCKETPOINT_DELETED
                data = {"id": 99}

                broadcast_ws_message(user_ids, event_type, data)

                assert mock_async_send.call_count == 3

    def test_broadcasts_to_correct_groups(self):
        """Test that message is sent to correct user groups."""
        mock_channel_layer = MagicMock()
        mock_async_send = MagicMock()

        with patch(
            "core.websocket.utils.get_channel_layer", return_value=mock_channel_layer
        ):
            with patch(
                "core.websocket.utils.async_to_sync", return_value=mock_async_send
            ):
                user_ids = [10, 20]
                event_type = WebSocketMessageType.PHOTO_DELETED
                data = {"id": 1}

                broadcast_ws_message(user_ids, event_type, data)

                calls = mock_async_send.call_args_list
                groups_called = [c[0][0] for c in calls]
                assert "user_10" in groups_called
                assert "user_20" in groups_called

    def test_handles_empty_user_list(self):
        """Test that function handles empty user list without error."""
        mock_channel_layer = MagicMock()
        mock_async_send = MagicMock()

        with patch(
            "core.websocket.utils.get_channel_layer", return_value=mock_channel_layer
        ):
            with patch(
                "core.websocket.utils.async_to_sync", return_value=mock_async_send
            ):
                broadcast_ws_message([], WebSocketMessageType.MESSAGE_CREATED, {})

                mock_async_send.assert_not_called()

    def test_broadcasts_same_data_to_all_users(self):
        """Test that identical data is sent to all users."""
        mock_channel_layer = MagicMock()
        mock_async_send = MagicMock()

        with patch(
            "core.websocket.utils.get_channel_layer", return_value=mock_channel_layer
        ):
            with patch(
                "core.websocket.utils.async_to_sync", return_value=mock_async_send
            ):
                user_ids = [1, 2]
                data = {"key": "shared_value"}

                broadcast_ws_message(
                    user_ids, WebSocketMessageType.SYSTEM_NOTIFICATION, data
                )

                calls = mock_async_send.call_args_list
                payloads = [c[0][1]["payload"]["data"] for c in calls]
                assert all(p == data for p in payloads)


class TestWebSocketMessageType:
    """Tests for WebSocketMessageType enum."""

    def test_all_required_types_exist(self):
        """Test that all required message types are defined."""
        required_types = [
            "MESSAGE_CREATED",
            "MESSAGE_DELETED",
            "MESSAGE_VIEWED",
            "USER_PRESENCE_CONNECTED",
            "USER_PRESENCE_DISCONNECTED",
            "BUCKETPOINT_CREATED",
            "BUCKETPOINT_DELETED",
            "BUCKETPOINT_UPDATED",
            "PHOTO_UPLOADED",
            "PHOTO_DELETED",
            "PHOTO_UPDATED",
            "ALBUM_CREATED",
            "ALBUM_DELETED",
            "ALBUM_UPDATED",
            "SYSTEM_NOTIFICATION",
        ]

        for msg_type in required_types:
            assert hasattr(WebSocketMessageType, msg_type), f"Missing type: {msg_type}"

    def test_enum_values_match_names(self):
        """Test that enum values match their names (convention)."""
        for member in WebSocketMessageType:
            assert member.value == member.name
