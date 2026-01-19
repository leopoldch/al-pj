"""
Pytest configuration and shared fixtures for backend tests.

This module provides reusable test fixtures following pytest best practices.
All fixtures are designed for isolation - each test gets fresh instances.
"""

import pytest
from unittest.mock import MagicMock, patch
from django.contrib.auth.models import User
from rest_framework.test import APIRequestFactory

from core.models import Album, Photo, Message, BucketPoint

TEST_USER_ID = 1
TEST_USER_EMAIL = "testuser@example.com"
TEST_USER_USERNAME = "testuser"
TEST_USER_FIRST_NAME = "Test"
TEST_USER_LAST_NAME = "User"
TEST_USER_PASSWORD = "testpassword123"

TEST_OTHER_USER_ID = 2
TEST_OTHER_USER_EMAIL = "otheruser@example.com"
TEST_OTHER_USER_USERNAME = "otheruser"

TEST_ALBUM_ID = 1
TEST_ALBUM_TITLE = "Test Album"
TEST_ALBUM_DESCRIPTION = "Test album description"
TEST_ALBUM_COVER_URL = "https://example.com/cover.jpg"

TEST_PHOTO_ID = 1
TEST_PHOTO_URL = "https://example.com/photo.jpg"
TEST_PHOTO_CAPTION = "Test photo caption"
TEST_PHOTO_LOCATION = "Paris, France"

TEST_MESSAGE_ID = 1
TEST_MESSAGE_CONTENT = "Test message content"

TEST_BUCKETPOINT_ID = 1
TEST_BUCKETPOINT_TITLE = "Test Bucket Point"
TEST_BUCKETPOINT_DESCRIPTION = "Test bucket point description"


@pytest.fixture
def mock_user():
    """Create a mock user for unit tests (no database)."""
    user = MagicMock(spec=User)
    user.id = TEST_USER_ID
    user.pk = TEST_USER_ID
    user.email = TEST_USER_EMAIL
    user.username = TEST_USER_USERNAME
    user.first_name = TEST_USER_FIRST_NAME
    user.last_name = TEST_USER_LAST_NAME
    user.get_full_name.return_value = f"{TEST_USER_FIRST_NAME} {TEST_USER_LAST_NAME}"
    user.is_authenticated = True
    return user


@pytest.fixture
def mock_other_user():
    """Create a mock 'other' user for tests involving multiple users."""
    user = MagicMock(spec=User)
    user.id = TEST_OTHER_USER_ID
    user.pk = TEST_OTHER_USER_ID
    user.email = TEST_OTHER_USER_EMAIL
    user.username = TEST_OTHER_USER_USERNAME
    user.first_name = "Other"
    user.last_name = "User"
    user.get_full_name.return_value = "Other User"
    user.is_authenticated = True
    return user


@pytest.fixture
def mock_album():
    """Create a mock Album for unit tests."""
    album = MagicMock(spec=Album)
    album.id = TEST_ALBUM_ID
    album.pk = TEST_ALBUM_ID
    album.title = TEST_ALBUM_TITLE
    album.description = TEST_ALBUM_DESCRIPTION
    album.cover_image = TEST_ALBUM_COVER_URL
    return album


@pytest.fixture
def mock_photo(mock_album):
    """Create a mock Photo for unit tests."""
    photo = MagicMock(spec=Photo)
    photo.id = TEST_PHOTO_ID
    photo.pk = TEST_PHOTO_ID
    photo.album = mock_album
    photo.image_url = TEST_PHOTO_URL
    photo.caption = TEST_PHOTO_CAPTION
    photo.location = TEST_PHOTO_LOCATION
    return photo


@pytest.fixture
def mock_message(mock_user):
    """Create a mock Message for unit tests."""
    message = MagicMock(spec=Message)
    message.id = TEST_MESSAGE_ID
    message.pk = TEST_MESSAGE_ID
    message.user = mock_user
    message.message = TEST_MESSAGE_CONTENT
    message.status = False
    return message


@pytest.fixture
def mock_bucketpoint():
    """Create a mock BucketPoint for unit tests."""
    bp = MagicMock(spec=BucketPoint)
    bp.id = TEST_BUCKETPOINT_ID
    bp.pk = TEST_BUCKETPOINT_ID
    bp.title = TEST_BUCKETPOINT_TITLE
    bp.description = TEST_BUCKETPOINT_DESCRIPTION
    bp.completed = False
    return bp


@pytest.fixture
def api_request_factory():
    """Provide DRF's APIRequestFactory for creating test requests."""
    return APIRequestFactory()


@pytest.fixture
def mock_request(mock_user):
    """Create a mock request with authenticated user."""
    request = MagicMock()
    request.user = mock_user
    request.data = {}
    request.FILES = {}
    return request


@pytest.fixture
def mock_image_file():
    """Create a mock image file for upload tests."""
    file = MagicMock()
    file.name = "test_image.jpg"
    file.content_type = "image/jpeg"
    file.size = 1024
    file.read.return_value = b"fake image content"
    return file


@pytest.fixture
def album_data():
    """Provide valid album creation data."""
    return {
        "title": TEST_ALBUM_TITLE,
        "description": TEST_ALBUM_DESCRIPTION,
    }


@pytest.fixture
def photo_data():
    """Provide valid photo creation data."""
    return {
        "caption": TEST_PHOTO_CAPTION,
        "location": TEST_PHOTO_LOCATION,
    }


@pytest.fixture
def message_data():
    """Provide valid message creation data."""
    return {
        "message": TEST_MESSAGE_CONTENT,
    }


@pytest.fixture
def bucketpoint_data():
    """Provide valid bucket point creation data."""
    return {
        "title": TEST_BUCKETPOINT_TITLE,
        "description": TEST_BUCKETPOINT_DESCRIPTION,
        "completed": False,
    }

@pytest.fixture
def mock_channel_layer():
    """Create a mock channel layer for WebSocket tests."""
    channel_layer = MagicMock()
    channel_layer.group_send = MagicMock()
    channel_layer.send = MagicMock()
    return channel_layer


@pytest.fixture
def patch_channel_layer(mock_channel_layer):
    """Patch get_channel_layer to return mock."""
    with patch("channels.layers.get_channel_layer", return_value=mock_channel_layer):
        yield mock_channel_layer

@pytest.fixture
def mock_photo_repository():
    """Create a mock photo repository for S3 operations."""
    repo = MagicMock()
    repo.save.return_value = "https://bucket.s3.amazonaws.com/test_image.jpg"
    repo.save_within_folder.return_value = "https://bucket.s3.amazonaws.com/1/test_image.jpg"
    repo.delete.return_value = True
    return repo


@pytest.fixture
def patch_photo_repository(mock_photo_repository):
    """Patch photo_repository with mock."""
    with patch("core.dependencies.photo_repository", mock_photo_repository):
        with patch("core.services.album_service.photo_repository", mock_photo_repository):
            with patch("core.services.photo_service.photo_repository", mock_photo_repository):
                yield mock_photo_repository


@pytest.fixture
def mock_redis():
    """Create a mock Redis client for presence tests."""
    redis_client = MagicMock()
    redis_client.sismember.return_value = True
    redis_client.sadd.return_value = 1
    redis_client.srem.return_value = 1
    return redis_client


@pytest.fixture
def patch_send_email():
    """Patch email sending functions."""
    with patch("core.utils.send_email") as mock_send:
        with patch("core.utils.send_formatted_mail") as mock_formatted:
            with patch("core.services.message_service.send_formatted_mail") as mock_service_mail:
                yield {
                    "send_email": mock_send,
                    "send_formatted_mail": mock_formatted,
                    "service_mail": mock_service_mail,
                }


@pytest.fixture
def serialized_message_data(mock_user):
    """Provide serialized message data as returned by MessageSerializer."""
    return {
        "id": TEST_MESSAGE_ID,
        "user": {
            "id": mock_user.id,
            "username": mock_user.username,
            "email": mock_user.email,
        },
        "name": mock_user.get_full_name(),
        "email": mock_user.email,
        "message": TEST_MESSAGE_CONTENT,
        "created_at": "2025-01-18T10:00:00Z",
        "status": False,
    }


@pytest.fixture
def serialized_bucketpoint_data():
    """Provide serialized bucket point data."""
    return {
        "id": TEST_BUCKETPOINT_ID,
        "title": TEST_BUCKETPOINT_TITLE,
        "description": TEST_BUCKETPOINT_DESCRIPTION,
        "completed": False,
        "created_at": "2025-01-18T10:00:00Z",
    }


@pytest.fixture
def serialized_album_data():
    """Provide serialized album data."""
    return {
        "id": TEST_ALBUM_ID,
        "title": TEST_ALBUM_TITLE,
        "description": TEST_ALBUM_DESCRIPTION,
        "cover_image": TEST_ALBUM_COVER_URL,
        "nb_photos": 0,
        "created_at": "2025-01-18T10:00:00Z",
        "updated_at": "2025-01-18T10:00:00Z",
    }


@pytest.fixture
def serialized_photo_data(serialized_album_data):
    """Provide serialized photo data."""
    return {
        "id": TEST_PHOTO_ID,
        "album": serialized_album_data,
        "image_url": TEST_PHOTO_URL,
        "caption": TEST_PHOTO_CAPTION,
        "location": TEST_PHOTO_LOCATION,
        "created_at": "2025-01-18T10:00:00Z",
        "updated_at": "2025-01-18T10:00:00Z",
    }
