import unittest
from unittest.mock import MagicMock, patch
from core.serializers.album import AlbumSerializer
from core.models.album import Album

TEST_ALBUM_ID = 1
TEST_TITLE = "Vacances Été"
TEST_NB_PHOTOS = 12
TEST_VALID_DATA = {"title": TEST_TITLE, "description": "Souvenirs"}

class TestAlbumSerializer(unittest.TestCase):

    def setUp(self):
        self.mock_request = MagicMock()
        self.mock_user = MagicMock()
        self.mock_request.user = self.mock_user
        self.context = {"request": self.mock_request}
        self.album_serializer = AlbumSerializer(context=self.context)

    @patch("core.serializers.album.Photo")
    def test_givenAlbumInstance_whenGetNbPhotos_thenShouldFilterPhotosByAlbum(self, mock_photo_model):
        mock_album = MagicMock(spec=Album)
        mock_qs = MagicMock()
        mock_photo_model.objects.filter.return_value = mock_qs
        
        self.album_serializer.get_nb_photos(mock_album)

        mock_photo_model.objects.filter.assert_called_once_with(album=mock_album)

    @patch("core.serializers.album.Photo")
    def test_givenAlbumInstance_whenGetNbPhotos_thenShouldReturnCount(self, mock_photo_model):
        mock_album = MagicMock(spec=Album)
        mock_qs = MagicMock()
        mock_photo_model.objects.filter.return_value = mock_qs
        mock_qs.count.return_value = TEST_NB_PHOTOS
        
        result = self.album_serializer.get_nb_photos(mock_album)

        self.assertEqual(result, TEST_NB_PHOTOS)

    def test_givenUnauthenticatedUser_whenCreate_thenShouldReturnNone(self):
        self.mock_user.is_authenticated = False
        
        result = self.album_serializer.create(TEST_VALID_DATA)

        self.assertIsNone(result)

    @patch("rest_framework.serializers.ModelSerializer.create")
    def test_givenAuthenticatedUser_whenCreate_thenShouldCallSuperCreate(self, mock_super_create):
        self.mock_user.is_authenticated = True
        
        self.album_serializer.create(TEST_VALID_DATA)

        mock_super_create.assert_called_once_with(TEST_VALID_DATA)

    @patch("rest_framework.serializers.ModelSerializer.create")
    def test_givenAuthenticatedUser_whenCreate_thenShouldReturnCreatedInstance(self, mock_super_create):
        self.mock_user.is_authenticated = True
        mock_instance = MagicMock()
        mock_super_create.return_value = mock_instance
        
        result = self.album_serializer.create(TEST_VALID_DATA)

        self.assertEqual(result, mock_instance)

    @patch("rest_framework.serializers.ModelSerializer.create")
    def test_givenNoRequestInContext_whenCreate_thenShouldCallSuperCreate(self, mock_super_create):
        serializer_without_request = AlbumSerializer(context={})
        
        serializer_without_request.create(TEST_VALID_DATA)

        mock_super_create.assert_called_once()

if __name__ == "__main__":
    unittest.main()