import unittest
from unittest.mock import MagicMock, patch, PropertyMock
from rest_framework.exceptions import ValidationError, NotFound

from core.services.bucketpoints_service import BucketPointService
from core.websocket.messages import WebSocketMessageType


TEST_USER_ID = 1
TEST_OTHER_USER_ID = 2
TEST_BUCKETPOINT_ID = 1
TEST_BUCKETPOINT_TITLE = "Visit Paris"
TEST_BUCKETPOINT_DESCRIPTION = "See the Eiffel Tower"
TEST_CREATED_AT = "2025-01-18T10:00:00Z"


class TestBucketPointServiceGetAll(unittest.TestCase):
    """Tests for BucketPointService.get_all method."""

    @patch("core.services.bucketpoints_service.BucketPointSerializer")
    @patch("core.services.bucketpoints_service.BucketPoint")
    def test_get_all_returns_serialized_bucket_points(
        self, mock_model, mock_serializer_class
    ):
        mock_queryset = MagicMock()
        mock_model.objects.all.return_value = mock_queryset
        serialized_data = [
            {"id": 1, "title": "First", "created_at": "2025-01-18T10:00:00Z"},
            {"id": 2, "title": "Second", "created_at": "2025-01-18T09:00:00Z"},
        ]
        mock_serializer_class.return_value.data = serialized_data

        result = BucketPointService.get_all()

        self.assertIsInstance(result, list)
        mock_model.objects.all.assert_called_once()

    @patch("core.services.bucketpoints_service.BucketPointSerializer")
    @patch("core.services.bucketpoints_service.BucketPoint")
    def test_get_all_returns_list_sorted_by_created_at_descending(
        self, mock_model, mock_serializer_class
    ):
        mock_queryset = MagicMock()
        mock_model.objects.all.return_value = mock_queryset
        serialized_data = [
            {"id": 1, "title": "Older", "created_at": "2025-01-17T10:00:00Z"},
            {"id": 2, "title": "Newer", "created_at": "2025-01-18T10:00:00Z"},
        ]
        mock_serializer_class.return_value.data = serialized_data

        result = BucketPointService.get_all()

        self.assertEqual(result[0]["title"], "Newer")
        self.assertEqual(result[1]["title"], "Older")

    @patch("core.services.bucketpoints_service.BucketPointSerializer")
    @patch("core.services.bucketpoints_service.BucketPoint")
    def test_get_all_when_empty_returns_empty_list(
        self, mock_model, mock_serializer_class
    ):
        mock_model.objects.all.return_value = MagicMock()
        mock_serializer_class.return_value.data = []

        result = BucketPointService.get_all()

        self.assertEqual(result, [])


class TestBucketPointServiceCreate(unittest.TestCase):

    def setUp(self):
        """Set up test fixtures."""
        self.valid_data = {
            "title": TEST_BUCKETPOINT_TITLE,
            "description": TEST_BUCKETPOINT_DESCRIPTION,
        }
        self.context = {"request": MagicMock()}
        self.serialized_data = {
            "id": TEST_BUCKETPOINT_ID,
            "title": TEST_BUCKETPOINT_TITLE,
            "description": TEST_BUCKETPOINT_DESCRIPTION,
            "completed": False,
            "created_at": TEST_CREATED_AT,
        }

    @patch("core.services.bucketpoints_service.send_ws_message_to_user")
    @patch("core.services.bucketpoints_service.User")
    @patch("core.services.bucketpoints_service.BucketPointSerializer")
    def test_create_with_valid_data_returns_serialized_bucket_point(
        self, mock_serializer_class, mock_user_model, mock_send_ws
    ):
        mock_serializer = MagicMock()
        mock_serializer.is_valid.return_value = True
        mock_bucket = MagicMock()
        mock_serializer.save.return_value = mock_bucket
        mock_serializer_class.return_value = mock_serializer
        mock_serializer_class.return_value.data = self.serialized_data
        mock_user_model.objects.all.return_value.values_list.return_value = []

        result = BucketPointService.create(self.valid_data, self.context)

        self.assertEqual(result["title"], TEST_BUCKETPOINT_TITLE)

    @patch("core.services.bucketpoints_service.send_ws_message_to_user")
    @patch("core.services.bucketpoints_service.User")
    @patch("core.services.bucketpoints_service.BucketPointSerializer")
    def test_create_with_valid_data_calls_serializer_save(
        self, mock_serializer_class, mock_user_model, mock_send_ws
    ):
        mock_serializer = MagicMock()
        mock_serializer.is_valid.return_value = True
        mock_serializer_class.return_value = mock_serializer
        mock_user_model.objects.all.return_value.values_list.return_value = []

        BucketPointService.create(self.valid_data, self.context)

        mock_serializer.save.assert_called_once()

    @patch("core.services.bucketpoints_service.BucketPointSerializer")
    def test_create_with_invalid_data_raises_validation_error(
        self, mock_serializer_class
    ):
        mock_serializer = MagicMock()
        mock_serializer.is_valid.return_value = False
        mock_serializer.errors = {"title": ["This field is required."]}
        mock_serializer_class.return_value = mock_serializer

        with self.assertRaises(ValidationError):
            BucketPointService.create({}, self.context)

    @patch("core.services.bucketpoints_service.send_ws_message_to_user")
    @patch("core.services.bucketpoints_service.User")
    @patch("core.services.bucketpoints_service.BucketPointSerializer")
    def test_create_broadcasts_bucketpoint_created_event(
        self, mock_serializer_class, mock_user_model, mock_send_ws
    ):
        mock_serializer = MagicMock()
        mock_serializer.is_valid.return_value = True
        mock_bucket = MagicMock()
        mock_serializer.save.return_value = mock_bucket
        mock_serializer_class.return_value = mock_serializer
        mock_serializer_class.return_value.data = self.serialized_data
        mock_user_model.objects.all.return_value.values_list.return_value = [
            TEST_USER_ID
        ]

        BucketPointService.create(self.valid_data, self.context)

        mock_send_ws.assert_called_once()
        call_args = mock_send_ws.call_args
        self.assertEqual(call_args[0][1], WebSocketMessageType.BUCKETPOINT_CREATED)


class TestBucketPointServiceUpdate(unittest.TestCase):

    def setUp(self):
        """Set up test fixtures."""
        self.update_data = {"completed": True}
        self.serialized_data = {
            "id": TEST_BUCKETPOINT_ID,
            "title": TEST_BUCKETPOINT_TITLE,
            "description": TEST_BUCKETPOINT_DESCRIPTION,
            "completed": True,
            "created_at": TEST_CREATED_AT,
        }

    @patch("core.services.bucketpoints_service.send_ws_message_to_user")
    @patch("core.services.bucketpoints_service.User")
    @patch("core.services.bucketpoints_service.BucketPointSerializer")
    @patch("core.services.bucketpoints_service.BucketPoint")
    def test_update_with_valid_id_returns_updated_data(
        self, mock_model, mock_serializer_class, mock_user_model, mock_send_ws
    ):
        mock_bucket = MagicMock()
        mock_model.objects.get.return_value = mock_bucket
        mock_serializer = MagicMock()
        mock_serializer.is_valid.return_value = True
        mock_serializer.save.return_value = mock_bucket
        mock_serializer_class.return_value = mock_serializer
        mock_serializer_class.return_value.data = self.serialized_data
        mock_user_model.objects.all.return_value.values_list.return_value = []

        result = BucketPointService.update(TEST_BUCKETPOINT_ID, self.update_data)

        self.assertEqual(result["completed"], True)

    @patch("core.services.bucketpoints_service.BucketPoint")
    def test_update_with_nonexistent_id_raises_not_found(self, mock_model):
        mock_model.DoesNotExist = Exception
        mock_model.objects.get.side_effect = mock_model.DoesNotExist

        with self.assertRaises(NotFound):
            BucketPointService.update(999, self.update_data)

    @patch("core.services.bucketpoints_service.BucketPointSerializer")
    @patch("core.services.bucketpoints_service.BucketPoint")
    def test_update_with_invalid_data_raises_validation_error(
        self, mock_model, mock_serializer_class
    ):
        mock_bucket = MagicMock()
        mock_model.objects.get.return_value = mock_bucket
        mock_serializer = MagicMock()
        mock_serializer.is_valid.return_value = False
        mock_serializer.errors = {"title": ["Invalid value."]}
        mock_serializer_class.return_value = mock_serializer

        with self.assertRaises(ValidationError):
            BucketPointService.update(TEST_BUCKETPOINT_ID, {"title": ""})

    @patch("core.services.bucketpoints_service.send_ws_message_to_user")
    @patch("core.services.bucketpoints_service.User")
    @patch("core.services.bucketpoints_service.BucketPointSerializer")
    @patch("core.services.bucketpoints_service.BucketPoint")
    def test_update_uses_partial_serialization(
        self, mock_model, mock_serializer_class, mock_user_model, mock_send_ws
    ):
        mock_bucket = MagicMock()
        mock_model.objects.get.return_value = mock_bucket
        mock_serializer = MagicMock()
        mock_serializer.is_valid.return_value = True
        mock_serializer_class.return_value = mock_serializer
        mock_user_model.objects.all.return_value.values_list.return_value = []

        BucketPointService.update(TEST_BUCKETPOINT_ID, self.update_data)

        first_call = mock_serializer_class.call_args_list[0]
        self.assertEqual(first_call[0][0], mock_bucket)
        self.assertEqual(first_call[1]["data"], self.update_data)
        self.assertEqual(first_call[1]["partial"], True)

    @patch("core.services.bucketpoints_service.send_ws_message_to_user")
    @patch("core.services.bucketpoints_service.User")
    @patch("core.services.bucketpoints_service.BucketPointSerializer")
    @patch("core.services.bucketpoints_service.BucketPoint")
    def test_update_broadcasts_bucketpoint_updated_event(
        self, mock_model, mock_serializer_class, mock_user_model, mock_send_ws
    ):
        mock_bucket = MagicMock()
        mock_model.objects.get.return_value = mock_bucket
        mock_serializer = MagicMock()
        mock_serializer.is_valid.return_value = True
        mock_serializer.save.return_value = mock_bucket
        mock_serializer_class.return_value = mock_serializer
        mock_serializer_class.return_value.data = self.serialized_data
        mock_user_model.objects.all.return_value.values_list.return_value = [
            TEST_USER_ID
        ]

        BucketPointService.update(TEST_BUCKETPOINT_ID, self.update_data)

        mock_send_ws.assert_called_once()
        call_args = mock_send_ws.call_args
        self.assertEqual(call_args[0][1], WebSocketMessageType.BUCKETPOINT_UPDATED)


class TestBucketPointServiceDelete(unittest.TestCase):

    @patch("core.services.bucketpoints_service.send_ws_message_to_user")
    @patch("core.services.bucketpoints_service.User")
    @patch("core.services.bucketpoints_service.BucketPoint")
    def test_delete_with_valid_id_deletes_bucket_point(
        self, mock_model, mock_user_model, mock_send_ws
    ):
        mock_bucket = MagicMock()
        mock_bucket.id = TEST_BUCKETPOINT_ID
        mock_model.objects.get.return_value = mock_bucket
        mock_user_model.objects.all.return_value.values_list.return_value = []

        BucketPointService.delete(TEST_BUCKETPOINT_ID)

        mock_bucket.delete.assert_called_once()

    @patch("core.services.bucketpoints_service.BucketPoint")
    def test_delete_with_nonexistent_id_raises_not_found(self, mock_model):
        mock_model.DoesNotExist = Exception
        mock_model.objects.get.side_effect = mock_model.DoesNotExist

        with self.assertRaises(NotFound):
            BucketPointService.delete(999)

    @patch("core.services.bucketpoints_service.send_ws_message_to_user")
    @patch("core.services.bucketpoints_service.User")
    @patch("core.services.bucketpoints_service.BucketPoint")
    def test_delete_broadcasts_bucketpoint_deleted_event_with_id(
        self, mock_model, mock_user_model, mock_send_ws
    ):
        mock_bucket = MagicMock()
        mock_bucket.id = TEST_BUCKETPOINT_ID
        mock_model.objects.get.return_value = mock_bucket
        mock_user_model.objects.all.return_value.values_list.return_value = [
            TEST_USER_ID
        ]

        BucketPointService.delete(TEST_BUCKETPOINT_ID)

        mock_send_ws.assert_called_once()
        call_args = mock_send_ws.call_args
        self.assertEqual(call_args[0][1], WebSocketMessageType.BUCKETPOINT_DELETED)
        self.assertEqual(call_args[0][2], {"id": TEST_BUCKETPOINT_ID})

    @patch("core.services.bucketpoints_service.send_ws_message_to_user")
    @patch("core.services.bucketpoints_service.User")
    @patch("core.services.bucketpoints_service.BucketPoint")
    def test_delete_returns_none(self, mock_model, mock_user_model, mock_send_ws):
        mock_bucket = MagicMock()
        mock_bucket.id = TEST_BUCKETPOINT_ID
        mock_model.objects.get.return_value = mock_bucket
        mock_user_model.objects.all.return_value.values_list.return_value = []

        result = BucketPointService.delete(TEST_BUCKETPOINT_ID)

        self.assertIsNone(result)


class TestBucketPointServiceBroadcastChange(unittest.TestCase):
    """Tests for BucketPointService._broadcast_change method."""

    @patch("core.services.bucketpoints_service.send_ws_message_to_user")
    @patch("core.services.bucketpoints_service.User")
    def test_broadcast_change_sends_to_all_users(self, mock_user_model, mock_send_ws):
        
        mock_user_model.objects.all.return_value.values_list.return_value = [
            TEST_USER_ID,
            TEST_OTHER_USER_ID,
        ]
        message_data = {"data": {"id": 1}}

        
        BucketPointService._broadcast_change(
            WebSocketMessageType.BUCKETPOINT_CREATED, message_data
        )

        
        self.assertEqual(mock_send_ws.call_count, 2)

    @patch("core.services.bucketpoints_service.send_ws_message_to_user")
    @patch("core.services.bucketpoints_service.User")
    def test_broadcast_change_when_no_users_does_not_send(
        self, mock_user_model, mock_send_ws
    ):
        
        mock_user_model.objects.all.return_value.values_list.return_value = []
        message_data = {"data": {"id": 1}}

        
        BucketPointService._broadcast_change(
            WebSocketMessageType.BUCKETPOINT_CREATED, message_data
        )

        
        mock_send_ws.assert_not_called()


if __name__ == "__main__":
    unittest.main()
