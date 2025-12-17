import unittest
from unittest.mock import MagicMock, patch
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate
from core.views.photos import PhotoView
from rest_framework.exceptions import ValidationError

TEST_USER_ID = 1
TEST_ALBUM_ID = 42
TEST_PHOTO_ID = 101
TEST_PHOTO_URL = "https://s3.amazonaws.com/bucket/photo.jpg"
TEST_PHOTO_DATA = {"caption": "Souvenir de vacances"}
TEST_RETURNED_PHOTOS = [{"id": TEST_PHOTO_ID, "image_url": TEST_PHOTO_URL, "caption": "Souvenir"}]
TEST_EXPECTED_GET_RESPONSE = {"photos": TEST_RETURNED_PHOTOS, "album_id": TEST_ALBUM_ID}

class TestPhotoView(unittest.TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = PhotoView()
        self.mock_user = MagicMock()
        self.mock_user.id = TEST_USER_ID

    @patch("core.views.photos.PhotoService")
    def test_givenAuthenticatedUser_whenGet_thenShouldCallServiceGetPhotosByAlbumId(self, mock_service):
        request = self.factory.get(f"/photos/{TEST_ALBUM_ID}/")
        force_authenticate(request, user=self.mock_user)
        self.view.request = request
        self.view.format_kwarg = None

        self.view.get(request, album_id=TEST_ALBUM_ID)

        mock_service.get_photos_by_album_id.assert_called_once_with(TEST_ALBUM_ID)

    @patch("core.views.photos.PhotoService")
    def test_givenServiceReturnsPhotos_whenGet_thenShouldReturn200(self, mock_service):
        request = self.factory.get(f"/photos/{TEST_ALBUM_ID}/")
        force_authenticate(request, user=self.mock_user)
        self.view.request = request
        self.view.format_kwarg = None
        mock_service.get_photos_by_album_id.return_value = TEST_RETURNED_PHOTOS

        response = self.view.get(request, album_id=TEST_ALBUM_ID)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch("core.views.photos.PhotoService")
    def test_givenServiceReturnsPhotos_whenGet_thenShouldReturnCorrectDataStructure(self, mock_service):
        request = self.factory.get(f"/photos/{TEST_ALBUM_ID}/")
        force_authenticate(request, user=self.mock_user)
        self.view.request = request
        self.view.format_kwarg = None
        mock_service.get_photos_by_album_id.return_value = TEST_RETURNED_PHOTOS

        response = self.view.get(request, album_id=TEST_ALBUM_ID)

        self.assertEqual(response.data, TEST_EXPECTED_GET_RESPONSE)

    @patch("core.views.photos.PhotoService")
    def test_givenValidData_whenPost_thenShouldCallServiceSavePhoto(self, mock_service):
        request = self.factory.post(f"/photos/{TEST_ALBUM_ID}/", TEST_PHOTO_DATA)
        request.user = self.mock_user
        request.data = TEST_PHOTO_DATA
        force_authenticate(request, user=self.mock_user)
        self.view.request = request
        self.view.format_kwarg = None

        self.view.post(request, album_id=TEST_ALBUM_ID)

        mock_service.save_photo.assert_called_once_with(TEST_ALBUM_ID, request)

    @patch("core.views.photos.PhotoService")
    def test_givenValidData_whenPost_thenShouldReturn201(self, mock_service):
        request = self.factory.post(f"/photos/{TEST_ALBUM_ID}/", TEST_PHOTO_DATA)
        request.user = self.mock_user
        request.data = TEST_PHOTO_DATA
        force_authenticate(request, user=self.mock_user)
        self.view.request = request
        self.view.format_kwarg = None

        response = self.view.post(request, album_id=TEST_ALBUM_ID)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @patch("core.views.photos.PhotoService")
    def test_givenServiceRaisesValidationError_whenPost_thenShouldRaiseValidationError(self, mock_service):
        request = self.factory.post(f"/photos/{TEST_ALBUM_ID}/", TEST_PHOTO_DATA)
        request.user = self.mock_user
        request.data = TEST_PHOTO_DATA
        force_authenticate(request, user=self.mock_user)
        self.view.request = request
        self.view.format_kwarg = None
        
        mock_service.save_photo.side_effect = ValidationError("Invalid image")

        with self.assertRaises(ValidationError):
            self.view.post(request, album_id=TEST_ALBUM_ID)

if __name__ == "__main__":
    unittest.main()