import unittest
from unittest.mock import MagicMock, patch
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate
from core.views.messages import PaginatedMessageView

TEST_USER_ID = 1

from rest_framework.request import Request


class TestPaginatedMessageView(unittest.TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = PaginatedMessageView()
        self.mock_user = MagicMock()
        self.mock_user.id = TEST_USER_ID

    @patch("core.views.messages.MessageService")
    @patch("core.views.messages.MessageSerializer")
    def test_givenAuthenticatedUser_whenGet_thenShouldReturnPaginatedResponse(
        self, mock_serializer, mock_service
    ):
        request = self.factory.get("/messages/paginated/")
        request = Request(request)  # Wrap WSGIRequest
        force_authenticate(request, user=self.mock_user)
        self.view.request = request
        self.view.format_kwarg = None

        # Mock 25 messages
        mock_messages = [MagicMock() for _ in range(25)]
        mock_service.getAll.return_value = mock_messages

        # Mock serializer data
        mock_serializer_instance = MagicMock()
        mock_serializer_instance.data = [
            {"id": i} for i in range(20)
        ]  # First page 20 items
        mock_serializer.return_value = mock_serializer_instance

        response = self.view.get(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("count", response.data)
        self.assertIn("next", response.data)
        self.assertIn("previous", response.data)
        self.assertIn("results", response.data)
        self.assertEqual(response.data["count"], 25)
        self.assertEqual(len(response.data["results"]), 20)
