import unittest
from unittest.mock import MagicMock, patch
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate
from core.views.albums import AlbumView

TEST_USER_ID = 1
TEST_ALBUM_ID = 123
TEST_ALBUM_NAME = "Vacances"
TEST_ALBUM_DATA = {"name": TEST_ALBUM_NAME}


class TestAlbumView(unittest.TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = AlbumView()
        self.mock_user = MagicMock()
        self.mock_user.id = TEST_USER_ID

    @patch("core.views.albums.AlbumService")
    @patch("core.views.albums.AlbumSerializer")
    def test_givenAuthenticatedUser_whenGet_thenShouldCallServiceGetAll(
        self, mock_serializer, mock_service
    ):
        request = self.factory.get("/albums/")
        force_authenticate(request, user=self.mock_user)
        self.view.request = request
        self.view.format_kwarg = None

        self.view.get(request)

        mock_service.getAll.assert_called_once()

    @patch("core.views.albums.AlbumService")
    @patch("core.views.albums.AlbumSerializer")
    def test_givenServiceReturnsAlbums_whenGet_thenShouldSerializeData(
        self, mock_serializer, mock_service
    ):
        request = self.factory.get("/albums/")
        force_authenticate(request, user=self.mock_user)
        self.view.request = request
        self.view.format_kwarg = None
        mock_albums = [MagicMock()]
        mock_service.getAll.return_value = mock_albums

        self.view.get(request)

        mock_serializer.assert_called_with(mock_albums, many=True)

    @patch("core.views.albums.AlbumService")
    @patch("core.views.albums.AlbumSerializer")
    def test_givenAuthenticatedUser_whenGet_thenShouldReturn200(
        self, mock_serializer, mock_service
    ):
        request = self.factory.get("/albums/")
        force_authenticate(request, user=self.mock_user)
        self.view.request = request
        self.view.format_kwarg = None

        response = self.view.get(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch("core.views.albums.AlbumService")
    def test_givenValidData_whenPost_thenShouldCallServiceCreateAlbum(
        self, mock_service
    ):
        request = self.factory.post("/albums/", TEST_ALBUM_DATA)
        request.data = TEST_ALBUM_DATA
        force_authenticate(request, user=self.mock_user)
        self.view.request = request
        self.view.format_kwarg = None

        self.view.post(request)

        mock_service.createAlbum.assert_called_once_with(request.data, request.FILES)

    @patch("core.views.albums.AlbumService")
    def test_givenValidData_whenPost_thenShouldReturn201(self, mock_service):
        request = self.factory.post("/albums/", TEST_ALBUM_DATA)
        request.data = TEST_ALBUM_DATA
        force_authenticate(request, user=self.mock_user)
        self.view.request = request
        self.view.format_kwarg = None

        response = self.view.post(request)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @patch("core.views.albums.AlbumService")
    def test_givenValidData_whenPut_thenShouldCallServiceModifyAlbum(
        self, mock_service
    ):
        request = self.factory.put(f"/albums/{TEST_ALBUM_ID}/", TEST_ALBUM_DATA)
        request.data = TEST_ALBUM_DATA  # CORRECTION
        force_authenticate(request, user=self.mock_user)
        self.view.request = request
        self.view.format_kwarg = None

        self.view.put(request, album_id=TEST_ALBUM_ID)

        mock_service.modifyAlbum.assert_called_once_with(
            TEST_ALBUM_ID, request.data, request.FILES
        )

    @patch("core.views.albums.AlbumService")
    def test_givenValidData_whenPut_thenShouldReturn200(self, mock_service):
        request = self.factory.put(f"/albums/{TEST_ALBUM_ID}/", TEST_ALBUM_DATA)
        request.data = TEST_ALBUM_DATA  # CORRECTION
        force_authenticate(request, user=self.mock_user)
        self.view.request = request
        self.view.format_kwarg = None

        response = self.view.put(request, album_id=TEST_ALBUM_ID)

        self.assertEqual(response.status_code, status.HTTP_200_OK)


if __name__ == "__main__":
    unittest.main()
