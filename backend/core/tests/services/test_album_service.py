import unittest
from unittest.mock import MagicMock, patch
from rest_framework.exceptions import ValidationError, NotFound

from core.services.album_service import AlbumService

TEST_ALBUM_ID = 1
TEST_ALBUM_TITLE = "Summer Vacation"
TEST_ALBUM_DESCRIPTION = "Photos from summer 2025"
TEST_COVER_IMAGE_URL = "https://bucket.s3.amazonaws.com/cover.jpg"
TEST_NEW_COVER_IMAGE_URL = "https://bucket.s3.amazonaws.com/new_cover.jpg"
TEST_FILE_NAME = "cover.jpg"


class TestAlbumServiceGetAll(unittest.TestCase):
    """Tests for AlbumService.getAll method."""

    @patch("core.services.album_service.Album")
    def test_getAll_returns_all_albums_queryset(self, mock_album_model):

        expected_queryset = MagicMock()
        mock_album_model.objects.all.return_value = expected_queryset

        result = AlbumService.getAll()

        self.assertEqual(result, expected_queryset)
        mock_album_model.objects.all.assert_called_once()

    @patch("core.services.album_service.Album")
    def test_getAll_when_empty_returns_empty_queryset(self, mock_album_model):

        empty_queryset = MagicMock()
        empty_queryset.__iter__ = MagicMock(return_value=iter([]))
        mock_album_model.objects.all.return_value = empty_queryset

        result = AlbumService.getAll()

        self.assertEqual(result, empty_queryset)


class TestAlbumServiceCreateAlbum(unittest.TestCase):
    """Tests for AlbumService.createAlbum method."""

    def setUp(self):
        """Set up test fixtures."""
        self.raw_data = {
            "title": TEST_ALBUM_TITLE,
            "description": TEST_ALBUM_DESCRIPTION,
        }
        self.mock_file = MagicMock()
        self.mock_file.name = TEST_FILE_NAME
        self.file_dict = {"image": self.mock_file}
        self.empty_file_dict = {}
        self.serialized_data = {
            "id": TEST_ALBUM_ID,
            "title": TEST_ALBUM_TITLE,
            "description": TEST_ALBUM_DESCRIPTION,
            "cover_image": TEST_COVER_IMAGE_URL,
            "nb_photos": 0,
        }

    @patch("core.services.album_service.AlbumSerializer")
    @patch("core.services.album_service.photo_repository")
    def test_createAlbum_with_image_uploads_to_s3(
        self, mock_photo_repo, mock_serializer_class
    ):

        mock_photo_repo.save.return_value = TEST_COVER_IMAGE_URL
        mock_serializer = MagicMock()
        mock_serializer.is_valid.return_value = True
        mock_serializer.data = self.serialized_data
        mock_serializer_class.return_value = mock_serializer

        AlbumService.createAlbum(self.raw_data, self.file_dict)

        mock_photo_repo.save.assert_called_once_with(self.mock_file)

    @patch("core.services.album_service.AlbumSerializer")
    @patch("core.services.album_service.photo_repository")
    def test_createAlbum_with_image_includes_cover_url_in_data(
        self, mock_photo_repo, mock_serializer_class
    ):

        mock_photo_repo.save.return_value = TEST_COVER_IMAGE_URL
        mock_serializer = MagicMock()
        mock_serializer.is_valid.return_value = True
        mock_serializer.data = self.serialized_data
        mock_serializer_class.return_value = mock_serializer

        AlbumService.createAlbum(self.raw_data, self.file_dict)

        call_args = mock_serializer_class.call_args
        data_passed = call_args[1]["data"]
        self.assertEqual(data_passed["cover_image"], TEST_COVER_IMAGE_URL)

    @patch("core.services.album_service.AlbumSerializer")
    @patch("core.services.album_service.photo_repository")
    def test_createAlbum_without_image_does_not_upload(
        self, mock_photo_repo, mock_serializer_class
    ):

        mock_serializer = MagicMock()
        mock_serializer.is_valid.return_value = True
        mock_serializer.data = self.serialized_data
        mock_serializer_class.return_value = mock_serializer

        AlbumService.createAlbum(self.raw_data, self.empty_file_dict)

        mock_photo_repo.save.assert_not_called()

    @patch("core.services.album_service.AlbumSerializer")
    @patch("core.services.album_service.photo_repository")
    def test_createAlbum_with_valid_data_returns_serialized_album(
        self, mock_photo_repo, mock_serializer_class
    ):

        mock_photo_repo.save.return_value = TEST_COVER_IMAGE_URL
        mock_serializer = MagicMock()
        mock_serializer.is_valid.return_value = True
        mock_serializer.data = self.serialized_data
        mock_serializer_class.return_value = mock_serializer

        result = AlbumService.createAlbum(self.raw_data, self.file_dict)

        self.assertEqual(result, self.serialized_data)

    @patch("core.services.album_service.AlbumSerializer")
    @patch("core.services.album_service.photo_repository")
    def test_createAlbum_calls_serializer_save(
        self, mock_photo_repo, mock_serializer_class
    ):

        mock_photo_repo.save.return_value = TEST_COVER_IMAGE_URL
        mock_serializer = MagicMock()
        mock_serializer.is_valid.return_value = True
        mock_serializer.data = self.serialized_data
        mock_serializer_class.return_value = mock_serializer

        AlbumService.createAlbum(self.raw_data, self.file_dict)

        mock_serializer.save.assert_called_once()

    @patch("core.services.album_service.AlbumSerializer")
    def test_createAlbum_with_invalid_data_raises_validation_error(
        self, mock_serializer_class
    ):

        mock_serializer = MagicMock()
        mock_serializer.is_valid.return_value = False
        mock_serializer.errors = {"title": ["This field is required."]}
        mock_serializer_class.return_value = mock_serializer

        with self.assertRaises(ValidationError):
            AlbumService.createAlbum({}, self.empty_file_dict)


class TestAlbumServiceModifyAlbum(unittest.TestCase):
    """Tests for AlbumService.modifyAlbum method."""

    def setUp(self):
        """Set up test fixtures."""
        self.raw_data = {
            "title": "Updated Title",
            "description": "Updated description",
        }
        self.mock_file = MagicMock()
        self.mock_file.name = TEST_FILE_NAME
        self.file_dict = {"image": self.mock_file}
        self.empty_file_dict = {}

        self.mock_album = MagicMock()
        self.mock_album.id = TEST_ALBUM_ID
        self.mock_album.cover_image = TEST_COVER_IMAGE_URL

        self.serialized_data = {
            "id": TEST_ALBUM_ID,
            "title": "Updated Title",
            "description": "Updated description",
            "cover_image": TEST_NEW_COVER_IMAGE_URL,
        }

    @patch("core.services.album_service.AlbumSerializer")
    @patch("core.services.album_service.photo_repository")
    @patch("core.services.album_service.get_object_or_404")
    def test_modifyAlbum_with_valid_id_returns_updated_album(
        self, mock_get_object, mock_photo_repo, mock_serializer_class
    ):

        mock_get_object.return_value = self.mock_album
        mock_photo_repo.delete.return_value = True
        mock_photo_repo.save.return_value = TEST_NEW_COVER_IMAGE_URL
        mock_serializer = MagicMock()
        mock_serializer.is_valid.return_value = True
        mock_serializer.data = self.serialized_data
        mock_serializer_class.return_value = mock_serializer

        result = AlbumService.modifyAlbum(TEST_ALBUM_ID, self.raw_data, self.file_dict)

        self.assertEqual(result, self.serialized_data)

    @patch("core.services.album_service.get_object_or_404")
    def test_modifyAlbum_without_image_raises_not_found(self, mock_get_object):

        mock_get_object.return_value = self.mock_album

        with self.assertRaises(NotFound):
            AlbumService.modifyAlbum(TEST_ALBUM_ID, self.raw_data, self.empty_file_dict)

    @patch("core.services.album_service.AlbumSerializer")
    @patch("core.services.album_service.photo_repository")
    @patch("core.services.album_service.get_object_or_404")
    def test_modifyAlbum_deletes_old_cover_image(
        self, mock_get_object, mock_photo_repo, mock_serializer_class
    ):

        mock_get_object.return_value = self.mock_album
        mock_photo_repo.delete.return_value = True
        mock_photo_repo.save.return_value = TEST_NEW_COVER_IMAGE_URL
        mock_serializer = MagicMock()
        mock_serializer.is_valid.return_value = True
        mock_serializer.data = self.serialized_data
        mock_serializer_class.return_value = mock_serializer

        AlbumService.modifyAlbum(TEST_ALBUM_ID, self.raw_data, self.file_dict)

        mock_photo_repo.delete.assert_called_once_with(TEST_COVER_IMAGE_URL)

    @patch("core.services.album_service.AlbumSerializer")
    @patch("core.services.album_service.photo_repository")
    @patch("core.services.album_service.get_object_or_404")
    def test_modifyAlbum_uploads_new_cover_image(
        self, mock_get_object, mock_photo_repo, mock_serializer_class
    ):

        mock_get_object.return_value = self.mock_album
        mock_photo_repo.delete.return_value = True
        mock_photo_repo.save.return_value = TEST_NEW_COVER_IMAGE_URL
        mock_serializer = MagicMock()
        mock_serializer.is_valid.return_value = True
        mock_serializer.data = self.serialized_data
        mock_serializer_class.return_value = mock_serializer

        AlbumService.modifyAlbum(TEST_ALBUM_ID, self.raw_data, self.file_dict)

        mock_photo_repo.save.assert_called_once_with(self.mock_file)

    @patch("core.services.album_service.AlbumSerializer")
    @patch("core.services.album_service.photo_repository")
    @patch("core.services.album_service.get_object_or_404")
    def test_modifyAlbum_uses_partial_serialization(
        self, mock_get_object, mock_photo_repo, mock_serializer_class
    ):

        mock_get_object.return_value = self.mock_album
        mock_photo_repo.delete.return_value = True
        mock_photo_repo.save.return_value = TEST_NEW_COVER_IMAGE_URL
        mock_serializer = MagicMock()
        mock_serializer.is_valid.return_value = True
        mock_serializer.data = self.serialized_data
        mock_serializer_class.return_value = mock_serializer

        AlbumService.modifyAlbum(TEST_ALBUM_ID, self.raw_data, self.file_dict)

        call_args = mock_serializer_class.call_args
        self.assertEqual(call_args[1]["partial"], True)

    @patch("core.services.album_service.AlbumSerializer")
    @patch("core.services.album_service.photo_repository")
    @patch("core.services.album_service.get_object_or_404")
    def test_modifyAlbum_with_invalid_data_raises_validation_error(
        self, mock_get_object, mock_photo_repo, mock_serializer_class
    ):

        mock_get_object.return_value = self.mock_album
        mock_photo_repo.delete.return_value = True
        mock_photo_repo.save.return_value = TEST_NEW_COVER_IMAGE_URL
        mock_serializer = MagicMock()
        mock_serializer.is_valid.return_value = False
        mock_serializer.errors = {"title": ["Invalid value."]}
        mock_serializer_class.return_value = mock_serializer

        with self.assertRaises(ValidationError):
            AlbumService.modifyAlbum(TEST_ALBUM_ID, {"title": ""}, self.file_dict)


class TestAlbumServiceReplaceCoverImage(unittest.TestCase):
    """Tests for AlbumService._replace_cover_image method."""

    def setUp(self):
        """Set up test fixtures."""
        self.data = {"title": "Test"}
        self.mock_file = MagicMock()
        self.mock_file.name = TEST_FILE_NAME
        self.file_dict = {"image": self.mock_file}

    @patch("core.services.album_service.photo_repository")
    def test_replace_cover_image_when_album_has_cover_deletes_old(
        self, mock_photo_repo
    ):

        mock_album = MagicMock()
        mock_album.cover_image = TEST_COVER_IMAGE_URL
        mock_photo_repo.save.return_value = TEST_NEW_COVER_IMAGE_URL

        AlbumService._replace_cover_image(self.data, mock_album, self.file_dict)

        mock_photo_repo.delete.assert_called_once_with(TEST_COVER_IMAGE_URL)

    @patch("core.services.album_service.photo_repository")
    def test_replace_cover_image_when_album_has_cover_uploads_new(
        self, mock_photo_repo
    ):

        mock_album = MagicMock()
        mock_album.cover_image = TEST_COVER_IMAGE_URL
        mock_photo_repo.save.return_value = TEST_NEW_COVER_IMAGE_URL

        AlbumService._replace_cover_image(self.data, mock_album, self.file_dict)

        mock_photo_repo.save.assert_called_once_with(self.mock_file)

    @patch("core.services.album_service.photo_repository")
    def test_replace_cover_image_returns_data_with_new_cover_url(self, mock_photo_repo):

        mock_album = MagicMock()
        mock_album.cover_image = TEST_COVER_IMAGE_URL
        mock_photo_repo.save.return_value = TEST_NEW_COVER_IMAGE_URL

        result = AlbumService._replace_cover_image(
            self.data, mock_album, self.file_dict
        )

        self.assertEqual(result["cover_image"], TEST_NEW_COVER_IMAGE_URL)

    @patch("core.services.album_service.photo_repository")
    def test_replace_cover_image_when_no_existing_cover_does_not_delete(
        self, mock_photo_repo
    ):

        mock_album = MagicMock()
        mock_album.cover_image = None

        result = AlbumService._replace_cover_image(
            self.data, mock_album, self.file_dict
        )

        mock_photo_repo.delete.assert_not_called()
        self.assertEqual(result, self.data)

    @patch("core.services.album_service.photo_repository")
    def test_replace_cover_image_when_empty_cover_does_not_delete(
        self, mock_photo_repo
    ):

        mock_album = MagicMock()
        mock_album.cover_image = ""

        result = AlbumService._replace_cover_image(
            self.data, mock_album, self.file_dict
        )

        mock_photo_repo.delete.assert_not_called()
        self.assertEqual(result, self.data)


if __name__ == "__main__":
    unittest.main()
