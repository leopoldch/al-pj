import unittest
from unittest.mock import MagicMock, patch
from core.serializers.user import UserSerializer
from django.contrib.auth.models import User

TEST_USER_ID = 1
TEST_USERNAME = "JeanDupont"
TEST_EMAIL = "jean@example.com"
TEST_DATE_JOINED = "2023-01-01T12:00:00Z"
TEST_VALID_DATA = {"username": TEST_USERNAME, "email": TEST_EMAIL}


class TestUserSerializer(unittest.TestCase):

    def setUp(self):
        self.mock_user = MagicMock(spec=User)
        self.mock_user.id = TEST_USER_ID
        self.mock_user.username = TEST_USERNAME
        self.mock_user.email = TEST_EMAIL
        self.mock_user.date_joined = TEST_DATE_JOINED

        self.serializer = UserSerializer(instance=self.mock_user)

    def test_givenUserInstance_whenSerialize_thenShouldContainId(self):
        data = self.serializer.data
        self.assertEqual(data["id"], TEST_USER_ID)

    def test_givenUserInstance_whenSerialize_thenShouldContainUsername(self):
        data = self.serializer.data
        self.assertEqual(data["username"], TEST_USERNAME)

    def test_givenUserInstance_whenSerialize_thenShouldContainEmail(self):
        data = self.serializer.data
        self.assertEqual(data["email"], TEST_EMAIL)

    def test_givenUserInstance_whenSerialize_thenShouldContainDateJoined(self):
        data = self.serializer.data
        self.assertEqual(data["date_joined"], TEST_DATE_JOINED)

    @patch("rest_framework.serializers.ModelSerializer.create")
    def test_givenValidData_whenCreate_thenShouldCallSuperCreate(
        self, mock_super_create
    ):
        serializer = UserSerializer(data=TEST_VALID_DATA)
        serializer.is_valid = MagicMock(return_value=True)

        serializer.create(TEST_VALID_DATA)

        mock_super_create.assert_called_once_with(TEST_VALID_DATA)

    @patch("rest_framework.serializers.ModelSerializer.create")
    def test_givenValidData_whenCreate_thenShouldReturnCreatedInstance(
        self, mock_super_create
    ):
        mock_instance = MagicMock()
        mock_super_create.return_value = mock_instance
        serializer = UserSerializer(data=TEST_VALID_DATA)

        result = serializer.create(TEST_VALID_DATA)

        self.assertEqual(result, mock_instance)


if __name__ == "__main__":
    unittest.main()
