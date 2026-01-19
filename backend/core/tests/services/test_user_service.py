import unittest
from unittest.mock import MagicMock, patch
from rest_framework.exceptions import NotFound

from core.services.user_service import UserService

TEST_USER_ID = 1
TEST_OTHER_USER_ID = 2
TEST_OTHER_USER_USERNAME = "otheruser"
TEST_OTHER_USER_FULL_NAME = "Other User"


class TestUserServiceGetPresenceData(unittest.TestCase):
    """Tests for UserService.getPresenceData method."""

    def setUp(self):
        """Set up test fixtures."""
        self.mock_other_user = MagicMock()
        self.mock_other_user.id = TEST_OTHER_USER_ID
        self.mock_other_user.username = TEST_OTHER_USER_USERNAME
        self.mock_other_user.get_full_name.return_value = TEST_OTHER_USER_FULL_NAME

    @patch("core.services.user_service.get_redis_client")
    @patch("core.services.user_service.User")
    @patch("core.services.user_service.get_channel_layer")
    def test_getPresenceData_when_user_online_returns_is_online_true(
        self, mock_get_channel, mock_user_model, mock_redis
    ):

        mock_get_channel.return_value = MagicMock()
        mock_user_model.objects.exclude.return_value.first.return_value = (
            self.mock_other_user
        )
        mock_redis.return_value.sismember.return_value = True

        result = UserService.getPresenceData(TEST_USER_ID)

        self.assertTrue(result["is_online"])

    @patch("core.services.user_service.get_redis_client")
    @patch("core.services.user_service.User")
    @patch("core.services.user_service.get_channel_layer")
    def test_getPresenceData_when_user_offline_returns_is_online_false(
        self, mock_get_channel, mock_user_model, mock_redis
    ):

        mock_get_channel.return_value = MagicMock()
        mock_user_model.objects.exclude.return_value.first.return_value = (
            self.mock_other_user
        )
        mock_redis.return_value.sismember.return_value = False

        result = UserService.getPresenceData(TEST_USER_ID)

        self.assertFalse(result["is_online"])

    @patch("core.services.user_service.get_redis_client")
    @patch("core.services.user_service.User")
    @patch("core.services.user_service.get_channel_layer")
    def test_getPresenceData_returns_other_user_name(
        self, mock_get_channel, mock_user_model, mock_redis
    ):

        mock_get_channel.return_value = MagicMock()
        mock_user_model.objects.exclude.return_value.first.return_value = (
            self.mock_other_user
        )
        mock_redis.return_value.sismember.return_value = True

        result = UserService.getPresenceData(TEST_USER_ID)

        self.assertEqual(result["name"], TEST_OTHER_USER_FULL_NAME)

    @patch("core.services.user_service.get_redis_client")
    @patch("core.services.user_service.User")
    @patch("core.services.user_service.get_channel_layer")
    def test_getPresenceData_returns_username_when_no_full_name(
        self, mock_get_channel, mock_user_model, mock_redis
    ):

        mock_get_channel.return_value = MagicMock()
        self.mock_other_user.get_full_name.return_value = ""
        mock_user_model.objects.exclude.return_value.first.return_value = (
            self.mock_other_user
        )
        mock_redis.return_value.sismember.return_value = True

        result = UserService.getPresenceData(TEST_USER_ID)

        self.assertEqual(result["name"], TEST_OTHER_USER_USERNAME)

    @patch("core.services.user_service.get_redis_client")
    @patch("core.services.user_service.User")
    @patch("core.services.user_service.get_channel_layer")
    def test_getPresenceData_returns_other_user_id(
        self, mock_get_channel, mock_user_model, mock_redis
    ):

        mock_get_channel.return_value = MagicMock()
        mock_user_model.objects.exclude.return_value.first.return_value = (
            self.mock_other_user
        )
        mock_redis.return_value.sismember.return_value = True

        result = UserService.getPresenceData(TEST_USER_ID)

        self.assertEqual(result["user_id"], TEST_OTHER_USER_ID)

    @patch("core.services.user_service.get_redis_client")
    @patch("core.services.user_service.User")
    @patch("core.services.user_service.get_channel_layer")
    def test_getPresenceData_excludes_current_user(
        self, mock_get_channel, mock_user_model, mock_redis
    ):

        mock_get_channel.return_value = MagicMock()
        mock_user_model.objects.exclude.return_value.first.return_value = (
            self.mock_other_user
        )
        mock_redis.return_value.sismember.return_value = True

        UserService.getPresenceData(TEST_USER_ID)

        mock_user_model.objects.exclude.assert_called_once_with(id=TEST_USER_ID)

    @patch("core.services.user_service.User")
    @patch("core.services.user_service.get_channel_layer")
    def test_getPresenceData_when_no_channel_layer_raises_exception(
        self, mock_get_channel, mock_user_model
    ):

        mock_get_channel.return_value = None

        with self.assertRaises(Exception) as context:
            UserService.getPresenceData(TEST_USER_ID)
        self.assertIn("channel layer", str(context.exception).lower())

    @patch("core.services.user_service.User")
    @patch("core.services.user_service.get_channel_layer")
    def test_getPresenceData_when_no_other_user_raises_not_found(
        self, mock_get_channel, mock_user_model
    ):

        mock_get_channel.return_value = MagicMock()
        mock_user_model.objects.exclude.return_value.first.return_value = None

        with self.assertRaises(NotFound):
            UserService.getPresenceData(TEST_USER_ID)

    @patch("core.services.user_service.get_redis_client")
    @patch("core.services.user_service.User")
    @patch("core.services.user_service.get_channel_layer")
    def test_getPresenceData_checks_redis_for_online_status(
        self, mock_get_channel, mock_user_model, mock_redis
    ):

        mock_get_channel.return_value = MagicMock()
        mock_user_model.objects.exclude.return_value.first.return_value = (
            self.mock_other_user
        )
        mock_redis.return_value.sismember.return_value = True

        UserService.getPresenceData(TEST_USER_ID)

        mock_redis.return_value.sismember.assert_called_once_with(
            "online_users", str(TEST_OTHER_USER_ID)
        )

    @patch("core.services.user_service.get_redis_client")
    @patch("core.services.user_service.User")
    @patch("core.services.user_service.get_channel_layer")
    def test_getPresenceData_when_redis_error_returns_is_online_false(
        self, mock_get_channel, mock_user_model, mock_redis
    ):

        from redis.exceptions import RedisError

        mock_get_channel.return_value = MagicMock()
        mock_user_model.objects.exclude.return_value.first.return_value = (
            self.mock_other_user
        )
        mock_redis.return_value.sismember.side_effect = RedisError("Connection refused")

        result = UserService.getPresenceData(TEST_USER_ID)

        self.assertFalse(result["is_online"])

    @patch("core.services.user_service.get_redis_client")
    @patch("core.services.user_service.User")
    @patch("core.services.user_service.get_channel_layer")
    def test_getPresenceData_redis_error_does_not_prevent_response(
        self, mock_get_channel, mock_user_model, mock_redis
    ):

        from redis.exceptions import RedisError

        mock_get_channel.return_value = MagicMock()
        mock_user_model.objects.exclude.return_value.first.return_value = (
            self.mock_other_user
        )
        mock_redis.return_value.sismember.side_effect = RedisError("Connection refused")

        result = UserService.getPresenceData(TEST_USER_ID)

        self.assertIn("name", result)
        self.assertIn("user_id", result)
        self.assertIn("is_online", result)


if __name__ == "__main__":
    unittest.main()
