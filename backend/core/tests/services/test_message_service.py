import unittest
from unittest.mock import MagicMock, patch
from rest_framework.exceptions import ValidationError

from core.services.message_service import MessageService
from core.websocket.messages import WebSocketMessageType

TEST_USER_ID = 1
TEST_OTHER_USER_ID = 2
TEST_MESSAGE_ID = 1
TEST_MESSAGE_CONTENT = "Test message content"
TEST_USER_EMAIL = "testuser@example.com"
TEST_USER_USERNAME = "testuser"


class TestMessageServiceCreateMessage(unittest.TestCase):
    """Tests for MessageService.create_message method."""

    def setUp(self):
        """Set up test fixtures."""
        self.mock_sender = MagicMock()
        self.mock_sender.id = TEST_USER_ID
        self.mock_sender.email = TEST_USER_EMAIL
        self.mock_sender.username = TEST_USER_USERNAME

        self.mock_receiver = MagicMock()
        self.mock_receiver.id = TEST_OTHER_USER_ID
        self.mock_receiver.email = "receiver@example.com"
        self.mock_receiver.username = "receiver"

        self.valid_data = {"message": TEST_MESSAGE_CONTENT}
        self.request_context = {"request": MagicMock()}

        self.serialized_data = {
            "id": TEST_MESSAGE_ID,
            "message": TEST_MESSAGE_CONTENT,
            "user": {"id": TEST_USER_ID},
            "created_at": "2025-01-18T10:00:00Z",
            "status": False,
        }

    @patch("core.services.message_service.send_formatted_mail")
    @patch("core.services.message_service.User")
    @patch("core.services.message_service.get_channel_layer")
    @patch("core.services.message_service.MessageSerializer")
    def test_create_message_with_valid_data_returns_serialized_message(
        self, mock_serializer_class, mock_get_channel, mock_user_model, mock_send_mail
    ):

        mock_serializer = MagicMock()
        mock_serializer.is_valid.return_value = True
        mock_serializer.data = self.serialized_data
        mock_serializer_class.return_value = mock_serializer
        mock_get_channel.return_value = None
        mock_user_model.objects.exclude.return_value.first.return_value = None

        result = MessageService.create_message(
            self.mock_sender, self.valid_data, self.request_context
        )

        self.assertEqual(result, self.serialized_data)

    @patch("core.services.message_service.send_formatted_mail")
    @patch("core.services.message_service.User")
    @patch("core.services.message_service.get_channel_layer")
    @patch("core.services.message_service.MessageSerializer")
    def test_create_message_with_valid_data_calls_serializer_save(
        self, mock_serializer_class, mock_get_channel, mock_user_model, mock_send_mail
    ):

        mock_serializer = MagicMock()
        mock_serializer.is_valid.return_value = True
        mock_serializer.data = self.serialized_data
        mock_serializer_class.return_value = mock_serializer
        mock_get_channel.return_value = None
        mock_user_model.objects.exclude.return_value.first.return_value = None

        MessageService.create_message(
            self.mock_sender, self.valid_data, self.request_context
        )

        mock_serializer.save.assert_called_once_with(user=self.mock_sender)

    @patch("core.services.message_service.MessageSerializer")
    def test_create_message_with_invalid_data_raises_validation_error(
        self, mock_serializer_class
    ):

        mock_serializer = MagicMock()
        mock_serializer.is_valid.return_value = False
        mock_serializer.errors = {"message": ["This field is required."]}
        mock_serializer_class.return_value = mock_serializer

        with self.assertRaises(ValidationError):
            MessageService.create_message(self.mock_sender, {}, self.request_context)

    @patch("core.services.message_service.send_formatted_mail")
    @patch("core.services.message_service.User")
    @patch("core.services.message_service.get_channel_layer")
    @patch("core.services.message_service.MessageSerializer")
    def test_create_message_when_receiver_exists_sends_email(
        self, mock_serializer_class, mock_get_channel, mock_user_model, mock_send_mail
    ):

        mock_serializer = MagicMock()
        mock_serializer.is_valid.return_value = True
        mock_serializer.data = self.serialized_data
        mock_serializer_class.return_value = mock_serializer
        mock_get_channel.return_value = None
        mock_user_model.objects.exclude.return_value.first.return_value = (
            self.mock_receiver
        )

        MessageService.create_message(
            self.mock_sender, self.valid_data, self.request_context
        )

        mock_send_mail.assert_called_once_with(
            str(self.mock_receiver.email), str(self.mock_receiver.username)
        )

    @patch("core.services.message_service.send_formatted_mail")
    @patch("core.services.message_service.User")
    @patch("core.services.message_service.get_channel_layer")
    @patch("core.services.message_service.MessageSerializer")
    def test_create_message_when_no_receiver_does_not_send_email(
        self, mock_serializer_class, mock_get_channel, mock_user_model, mock_send_mail
    ):

        mock_serializer = MagicMock()
        mock_serializer.is_valid.return_value = True
        mock_serializer.data = self.serialized_data
        mock_serializer_class.return_value = mock_serializer
        mock_get_channel.return_value = None
        mock_user_model.objects.exclude.return_value.first.return_value = None

        MessageService.create_message(
            self.mock_sender, self.valid_data, self.request_context
        )

        mock_send_mail.assert_not_called()

    @patch("core.services.message_service.send_formatted_mail")
    @patch("core.services.message_service.User")
    @patch("core.services.message_service.get_channel_layer")
    @patch("core.services.message_service.MessageSerializer")
    def test_create_message_when_email_fails_does_not_raise(
        self, mock_serializer_class, mock_get_channel, mock_user_model, mock_send_mail
    ):

        mock_serializer = MagicMock()
        mock_serializer.is_valid.return_value = True
        mock_serializer.data = self.serialized_data
        mock_serializer_class.return_value = mock_serializer
        mock_get_channel.return_value = None
        mock_user_model.objects.exclude.return_value.first.return_value = (
            self.mock_receiver
        )
        mock_send_mail.side_effect = Exception("SMTP Error")

        result = MessageService.create_message(
            self.mock_sender, self.valid_data, self.request_context
        )
        self.assertEqual(result, self.serialized_data)


class TestMessageServiceNotifyRecipients(unittest.TestCase):
    """Tests for MessageService._notify_recipients method."""

    def setUp(self):
        """Set up test fixtures."""
        self.mock_sender = MagicMock()
        self.mock_sender.id = TEST_USER_ID
        self.mock_sender.email = TEST_USER_EMAIL
        self.mock_sender.username = TEST_USER_USERNAME

        self.message_payload = {
            "id": TEST_MESSAGE_ID,
            "message": TEST_MESSAGE_CONTENT,
        }

    @patch("core.services.message_service.send_ws_message_to_user")
    @patch("core.services.message_service.User")
    @patch("core.services.message_service.get_channel_layer")
    def test_notify_recipients_when_channel_layer_exists_sends_to_all(
        self, mock_get_channel, mock_user_model, mock_send_ws
    ):

        mock_get_channel.return_value = MagicMock()
        mock_user_model.objects.all.return_value.values_list.return_value = [
            TEST_USER_ID,
            TEST_OTHER_USER_ID,
        ]

        MessageService._notify_recipients(
            self.mock_sender,
            self.message_payload,
            WebSocketMessageType.MESSAGE_CREATED,
        )

        self.assertEqual(mock_send_ws.call_count, 2)

        # Verify calls were made for both users
        expected_call_args_1 = (
            TEST_USER_ID,
            WebSocketMessageType.MESSAGE_CREATED,
            {
                "message": self.message_payload,
                "sender": {
                    "id": self.mock_sender.id,
                    "username": self.mock_sender.username,
                    "email": self.mock_sender.email,
                },
            },
        )
        expected_call_args_2 = (
            TEST_OTHER_USER_ID,
            WebSocketMessageType.MESSAGE_CREATED,
            {
                "message": self.message_payload,
                "sender": {
                    "id": self.mock_sender.id,
                    "username": self.mock_sender.username,
                    "email": self.mock_sender.email,
                },
            },
        )

        mock_send_ws.assert_any_call(*expected_call_args_1)
        mock_send_ws.assert_any_call(*expected_call_args_2)

    @patch("core.services.message_service.send_ws_message_to_user")
    @patch("core.services.message_service.get_channel_layer")
    def test_notify_recipients_when_no_channel_layer_does_not_send(
        self, mock_get_channel, mock_send_ws
    ):

        mock_get_channel.return_value = None

        MessageService._notify_recipients(
            self.mock_sender,
            self.message_payload,
            WebSocketMessageType.MESSAGE_CREATED,
        )

        mock_send_ws.assert_not_called()

    @patch("core.services.message_service.send_ws_message_to_user")
    @patch("core.services.message_service.User")
    @patch("core.services.message_service.get_channel_layer")
    def test_notify_recipients_includes_sender_in_recipients_list(
        self, mock_get_channel, mock_user_model, mock_send_ws
    ):

        mock_get_channel.return_value = MagicMock()
        mock_user_model.objects.all.return_value.values_list.return_value = [
            TEST_USER_ID,
        ]

        MessageService._notify_recipients(
            self.mock_sender,
            self.message_payload,
            WebSocketMessageType.MESSAGE_CREATED,
        )

        mock_send_ws.assert_called_once_with(
            TEST_USER_ID,
            WebSocketMessageType.MESSAGE_CREATED,
            {
                "message": self.message_payload,
                "sender": {
                    "id": self.mock_sender.id,
                    "username": self.mock_sender.username,
                    "email": self.mock_sender.email,
                },
            },
        )


class TestMessageServiceDelete(unittest.TestCase):
    """Tests for MessageService.delete method."""

    def setUp(self):
        """Set up test fixtures."""
        self.mock_user = MagicMock()
        self.mock_user.id = TEST_USER_ID

        self.mock_message = MagicMock()
        self.mock_message.id = TEST_MESSAGE_ID
        self.mock_message.user = self.mock_user
        self.mock_message.message = TEST_MESSAGE_CONTENT

    @patch("core.services.message_service.MessageSerializer")
    @patch("core.services.message_service.get_channel_layer")
    @patch("core.services.message_service.Message")
    def test_delete_with_valid_id_and_owner_returns_true(
        self, mock_message_model, mock_get_channel, mock_serializer_class
    ):

        mock_message_model.objects.get.return_value = self.mock_message
        mock_get_channel.return_value = None
        mock_serializer_class.return_value.data = {}

        result = MessageService.delete(TEST_MESSAGE_ID, self.mock_user)

        self.assertTrue(result)

    @patch("core.services.message_service.MessageSerializer")
    @patch("core.services.message_service.get_channel_layer")
    @patch("core.services.message_service.Message")
    def test_delete_with_valid_id_and_owner_deletes_message(
        self, mock_message_model, mock_get_channel, mock_serializer_class
    ):

        mock_message_model.objects.get.return_value = self.mock_message
        mock_get_channel.return_value = None
        mock_serializer_class.return_value.data = {}

        MessageService.delete(TEST_MESSAGE_ID, self.mock_user)

        self.mock_message.delete.assert_called_once()

    @patch("core.services.message_service.Message")
    def test_delete_with_nonexistent_id_returns_false(self, mock_message_model):
        mock_message_model.DoesNotExist = Exception
        mock_message_model.objects.get.side_effect = mock_message_model.DoesNotExist

        result = MessageService.delete(999, self.mock_user)

        self.assertFalse(result)

    @patch("core.services.message_service.send_ws_message_to_user")
    @patch("core.services.message_service.User")
    @patch("core.services.message_service.MessageSerializer")
    @patch("core.services.message_service.get_channel_layer")
    @patch("core.services.message_service.Message")
    def test_delete_with_valid_id_broadcasts_deletion(
        self,
        mock_message_model,
        mock_get_channel,
        mock_serializer_class,
        mock_user_model,
        mock_send_ws,
    ):

        mock_message_model.objects.get.return_value = self.mock_message
        mock_get_channel.return_value = MagicMock()
        serialized_data = {"id": TEST_MESSAGE_ID}
        mock_serializer_class.return_value.data = serialized_data
        mock_user_model.objects.all.return_value.values_list.return_value = [
            TEST_OTHER_USER_ID
        ]

        MessageService.delete(TEST_MESSAGE_ID, self.mock_user)

        mock_send_ws.assert_called_once()
        call_args = mock_send_ws.call_args
        self.assertEqual(call_args[0][0], TEST_OTHER_USER_ID)
        self.assertEqual(call_args[0][1], WebSocketMessageType.MESSAGE_DELETED)


if __name__ == "__main__":
    unittest.main()
