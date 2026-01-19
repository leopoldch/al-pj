import unittest
from unittest.mock import MagicMock, patch
from core.serializers.bucketpoint import BucketPointSerializer

TEST_TITLE = "Saut en parachute"
TEST_DESCRIPTION = "Depuis un avion"
TEST_VALID_DATA = {
    "title": TEST_TITLE,
    "description": TEST_DESCRIPTION,
    "completed": False,
}


class TestBucketPointSerializer(unittest.TestCase):

    def setUp(self):
        self.mock_request = MagicMock()
        self.mock_user = MagicMock()
        self.mock_request.user = self.mock_user
        self.context = {"request": self.mock_request}
        self.serializer = BucketPointSerializer(context=self.context)

    def test_givenUnauthenticatedUser_whenCreate_thenShouldReturnNone(self):
        self.mock_user.is_authenticated = False

        result = self.serializer.create(TEST_VALID_DATA)

        self.assertIsNone(result)

    @patch("rest_framework.serializers.ModelSerializer.create")
    def test_givenAuthenticatedUser_whenCreate_thenShouldCallSuperCreate(
        self, mock_super_create
    ):
        self.mock_user.is_authenticated = True

        self.serializer.create(TEST_VALID_DATA)

        mock_super_create.assert_called_once_with(TEST_VALID_DATA)

    @patch("rest_framework.serializers.ModelSerializer.create")
    def test_givenAuthenticatedUser_whenCreate_thenShouldReturnCreatedInstance(
        self, mock_super_create
    ):
        self.mock_user.is_authenticated = True
        mock_instance = MagicMock()
        mock_super_create.return_value = mock_instance

        result = self.serializer.create(TEST_VALID_DATA)

        self.assertEqual(result, mock_instance)

    @patch("rest_framework.serializers.ModelSerializer.create")
    def test_givenNoRequestInContext_whenCreate_thenShouldCallSuperCreate(
        self, mock_super_create
    ):
        serializer_no_context = BucketPointSerializer(context={})

        serializer_no_context.create(TEST_VALID_DATA)

        mock_super_create.assert_called_once_with(TEST_VALID_DATA)


if __name__ == "__main__":
    unittest.main()
