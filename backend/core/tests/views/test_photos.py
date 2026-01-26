from django.test import TestCase
from unittest.mock import patch
from rest_framework.test import APIRequestFactory, force_authenticate
from rest_framework import status
from core.views.photos import PhotoDetailView
from django.contrib.auth.models import User


class TestPhotoDetailView(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(username="testuser", password="password")
        self.view = PhotoDetailView.as_view()

    @patch("core.services.PhotoService.delete_photo")
    def test_delete_photo(self, mock_delete):
        request = self.factory.delete("/photos/1/1/")
        force_authenticate(request, user=self.user)

        response = self.view(request, album_id=1, photo_id=1)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        mock_delete.assert_called_once_with(photo_id=1, album_id=1)

    @patch("core.services.PhotoService.update_photo")
    def test_patch_photo(self, mock_update):
        data = {"caption": "Updated Caption"}
        mock_update.return_value = {"id": 1, "caption": "Updated Caption"}

        request = self.factory.patch("/photos/1/1/", data, format="json")
        force_authenticate(request, user=self.user)

        response = self.view(request, album_id=1, photo_id=1)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["photo"]["caption"], "Updated Caption")
        mock_update.assert_called_once_with(photo_id=1, album_id=1, data=data)
