import unittest
from unittest.mock import MagicMock, patch
from core.serializers.message import MessageSerializer
from core.models.message import Message
from django.contrib.auth.models import User

TEST_MESSAGE_ID = 10
TEST_CONTENT = "Hello World"
TEST_USERNAME = "JeanDupont"
TEST_EMAIL = "jean@example.com"
TEST_VALID_DATA = {"message": TEST_CONTENT}

class TestMessageSerializer(unittest.TestCase):

    def setUp(self):
        self.mock_request = MagicMock()
        self.mock_user = MagicMock(spec=User)
        self.mock_user.username = TEST_USERNAME
        self.mock_user.email = TEST_EMAIL
        self.mock_user.get_full_name = TEST_USERNAME
        
        self.mock_request.user = self.mock_user
        self.context = {"request": self.mock_request}
        self.serializer = MessageSerializer(context=self.context)

    def test_givenMessageInstance_whenSerialize_thenShouldContainExpectedFields(self):
        mock_message = MagicMock(spec=Message)
        mock_message.id = TEST_MESSAGE_ID
        mock_message.message = TEST_CONTENT
        mock_message.user = self.mock_user
        mock_message.created_at = "2023-01-01"
        mock_message.status = False
        
        serializer = MessageSerializer(instance=mock_message)
        data = serializer.data

        self.assertEqual(data["message"], TEST_CONTENT)
        self.assertEqual(data["email"], TEST_EMAIL)
        self.assertEqual(data["name"], TEST_USERNAME)

    @patch("rest_framework.serializers.ModelSerializer.create")
    def test_givenAuthenticatedUser_whenCreate_thenShouldAddUserToValidatedData(self, mock_super_create):
        self.mock_user.is_authenticated = True
        validated_data = TEST_VALID_DATA.copy()
        
        self.serializer.create(validated_data)

        expected_data = TEST_VALID_DATA.copy()
        expected_data["user"] = self.mock_user
        mock_super_create.assert_called_once_with(expected_data)

    @patch("rest_framework.serializers.ModelSerializer.create")
    def test_givenUnauthenticatedUser_whenCreate_thenShouldNotAddUserToValidatedData(self, mock_super_create):
        self.mock_user.is_authenticated = False
        validated_data = TEST_VALID_DATA.copy()
        
        self.serializer.create(validated_data)

        mock_super_create.assert_called_once_with(TEST_VALID_DATA)

    @patch("rest_framework.serializers.ModelSerializer.create")
    def test_givenNoRequestInContext_whenCreate_thenShouldNotAddUserToValidatedData(self, mock_super_create):
        serializer_no_context = MessageSerializer(context={})
        validated_data = TEST_VALID_DATA.copy()
        
        serializer_no_context.create(validated_data)

        mock_super_create.assert_called_once_with(TEST_VALID_DATA)

if __name__ == "__main__":
    unittest.main()