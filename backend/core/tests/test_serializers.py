from django.test import TestCase
from django.contrib.auth.models import AnonymousUser, User
from rest_framework.test import APIRequestFactory
from core.serializers import MessageSerializer, BucketPointSerializer
from core.models import Message, BucketPoint

class MessageSerializerTest(TestCase):
    def test_create_sets_user_fields(self):
        user = User.objects.create_user(username="u", email="u@example.com", password="p")
        factory = APIRequestFactory()
        request = factory.post("/", {"message": "hi"})
        request.user = user
        serializer = MessageSerializer(data={"message": "hello"}, context={"request": request})
        self.assertTrue(serializer.is_valid(), serializer.errors)
        message = serializer.save()
        self.assertEqual(message.user, user)
        self.assertEqual(message.name, user.username)
        self.assertEqual(message.email, user.email)
        self.assertEqual(Message.objects.count(), 1)


class BucketPointSerializerTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

    def test_create_requires_auth(self):
        request = self.factory.post("/", {"title": "t", "description": "d"})
        request.user = AnonymousUser()
        serializer = BucketPointSerializer(data={"title": "t", "description": "d"}, context={"request": request})
        self.assertTrue(serializer.is_valid(), serializer.errors)
        with self.assertRaises(AssertionError):
            serializer.save()
        self.assertEqual(BucketPoint.objects.count(), 0)

    def test_create_authenticated(self):
        user = User.objects.create_user("u", password="p")
        request = self.factory.post("/", {"title": "t", "description": "d"})
        request.user = user
        serializer = BucketPointSerializer(data={"title": "t", "description": "d"}, context={"request": request})
        self.assertTrue(serializer.is_valid(), serializer.errors)
        result = serializer.save()
        self.assertIsInstance(result, BucketPoint)
        self.assertEqual(BucketPoint.objects.count(), 1)


class ModelStrTest(TestCase):
    def test_str_methods(self):
        user = User.objects.create_user("u", email="e@example.com", password="p")
        msg = Message.objects.create(user=user, name="n", email="e@example.com", message="hi")
        bp = BucketPoint.objects.create(title="title", description="d")
        self.assertIn("Message from", str(msg))
        self.assertEqual(str(bp), "title")
