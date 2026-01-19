from django.test import SimpleTestCase
from unittest.mock import patch, MagicMock
from core.interface.aws import AwsPhotoSaver


class TestAwsPhotoSaver(SimpleTestCase):
    @patch("core.interface.aws.boto3")
    def test_save_within_folder(self, mock_boto3):
        mock_client = MagicMock()
        mock_boto3.client.return_value = mock_client

        repo = AwsPhotoSaver()
        file = MagicMock()
        file.name = "test.jpg"

        # Test success
        result = repo.save_within_folder(file, "123")
        self.assertIn("https://", result)
        self.assertIn("123/", str(mock_client.upload_fileobj.call_args))
        mock_client.upload_fileobj.assert_called_once()

    @patch("core.interface.aws.boto3")
    def test_delete(self, mock_boto3):
        mock_client = MagicMock()
        mock_boto3.client.return_value = mock_client

        repo = AwsPhotoSaver()

        repo.delete("https://bucket.s3.amazonaws.com/folder/photo.jpg")

        mock_client.delete_object.assert_called_once()
        call_args = mock_client.delete_object.call_args
        self.assertIn("photo.jpg", call_args[1]["Key"])
