from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from core.models import Message, BucketPoint

class AuthMixin:
    def authenticate(self, user: User):
        refresh = RefreshToken.for_user(user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")

class ProfileViewTest(APITestCase, AuthMixin):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="pass"
        )

    def test_profile_requires_auth(self):
        url = reverse("user_profile")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)

    def test_profile_returns_user(self):
        self.authenticate(self.user)
        url = reverse("user_profile")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["username"], self.user.username)

class MessageViewTest(APITestCase, AuthMixin):
    def setUp(self):
        self.user = User.objects.create_user(
            username="user", email="user@example.com", password="pass"
        )
        self.authenticate(self.user)

    def test_create_and_list_messages(self):
        url = reverse("user_messages")
        response = self.client.post(url, {"message": "Hello"}, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Message.objects.count(), 1)

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

class BucketPointViewTest(APITestCase, AuthMixin):
    def setUp(self):
        self.user = User.objects.create_user(
            username="bpuser", email="bp@example.com", password="pass"
        )
        self.authenticate(self.user)

    def test_crud_bucketpoint(self):
        list_url = reverse("bucket_points")
        create_resp = self.client.post(
            list_url,
            {"title": "T", "description": "D", "completed": False},
            format="json",
        )
        self.assertEqual(create_resp.status_code, 201)
        bp_id = create_resp.data["id"]

        list_resp = self.client.get(list_url)
        self.assertEqual(list_resp.status_code, 200)
        self.assertEqual(len(list_resp.data), 1)

        detail_url = reverse("bucket_points", kwargs={"pk": bp_id})
        update_resp = self.client.put(
            detail_url,
            {"title": "new", "description": "D", "completed": True},
            format="json",
        )
        self.assertEqual(update_resp.status_code, 200)

        delete_resp = self.client.delete(detail_url)
        self.assertEqual(delete_resp.status_code, 204)
        self.assertEqual(BucketPoint.objects.count(), 0)
