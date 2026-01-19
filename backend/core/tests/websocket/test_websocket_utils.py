from django.test import SimpleTestCase
from unittest.mock import patch, MagicMock
from core.websocket.utils import send_ws_message_to_user, broadcast_ws_message
from core.websocket.messages import WebSocketMessageType

class TestWebSocketUtils(SimpleTestCase):
    @patch("core.websocket.utils.get_channel_layer")
    @patch("core.websocket.utils.async_to_sync")
    def test_send_ws_message_to_user_success(self, mock_async_to_sync, mock_get_channel_layer):
        mock_channel_layer = MagicMock()
        mock_get_channel_layer.return_value = mock_channel_layer
        mock_send = MagicMock()
        mock_async_to_sync.return_value = mock_send
        
        user_id = 1
        event_type = "TEST_EVENT"
        data = {"key": "value"}
        
        send_ws_message_to_user(user_id, event_type, data)
        
        mock_async_to_sync.assert_called_once_with(mock_channel_layer.group_send)
        mock_send.assert_called_once_with(
            "user_1",
            {
                "type": "send.message",
                "payload": {
                    "type": "TEST_EVENT",
                    "data": {"key": "value"}
                }
            }
        )

    @patch("core.websocket.utils.get_channel_layer")
    def test_send_ws_message_to_user_no_channel_layer(self, mock_get_channel_layer):
        mock_get_channel_layer.return_value = None
        
        result = send_ws_message_to_user(1, "TEST", {})
        
        self.assertIsNone(result)

    @patch("core.websocket.utils.send_ws_message_to_user")
    def test_broadcast_ws_message(self, mock_send_single):
        user_ids = [1, 2, 3]
        event_type = WebSocketMessageType.MESSAGE_CREATED
        data = {"id": 1}
        
        broadcast_ws_message(user_ids, event_type, data)
        
        self.assertEqual(mock_send_single.call_count, 3)
        mock_send_single.assert_any_call(1, event_type, data)
        mock_send_single.assert_any_call(2, event_type, data)
        mock_send_single.assert_any_call(3, event_type, data)
