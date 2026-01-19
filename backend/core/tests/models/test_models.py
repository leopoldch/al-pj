from django.test import TestCase
from django.contrib.auth.models import User
from core.models import Message, Photo, Album, BucketPoint
from datetime import datetime


class TestModels(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.album = Album.objects.create(title="Test Album")

    def test_message_str(self):
        message = Message.objects.create(user=self.user, message="Hello World")
        # Message str includes timestamp, so we just check the prefix
        self.assertTrue(
            str(message).startswith(f"Message from {self.user.username} at ")
        )

    def test_album_str(self):
        self.assertEqual(str(self.album), "Test Album")

    def test_photo_str(self):
        photo = Photo.objects.create(
            album=self.album,
            image_url="http://example.com/image.jpg",
            caption="Test Photo",
        )
        self.assertEqual(str(photo), "Photo in Test Album - Test Photo")

    def test_photo_str_no_caption(self):
        photo = Photo.objects.create(
            album=self.album, image_url="http://example.com/image.jpg"
        )
        self.assertEqual(str(photo), "Photo in Test Album - No Caption")

    def test_bucketpoint_str(self):
        bp = BucketPoint.objects.create(title="Test Bucket Point")
        self.assertEqual(str(bp), "Test Bucket Point")
