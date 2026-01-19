import unittest
from unittest.mock import MagicMock, patch
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate
from core.views.users import ProfileView, PresenceIndicatorView

TEST_USER_ID = 1
TEST_USERNAME = "JeanDupont"
TEST_PRESENCE_DATA = {"is_online": True, "name": "Alice", "user_id": 2}


class TestProfileView(unittest.TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = ProfileView()
        self.mock_user = MagicMock()
        self.mock_user.id = TEST_USER_ID
        self.mock_user.username = TEST_USERNAME

    @patch("core.views.users.UserSerializer")
    def test_givenAuthenticatedUser_whenGet_thenShouldSerializeRequestUser(
        self, mock_serializer
    ):
        request = self.factory.get("/profile/")
        request.user = self.mock_user
        force_authenticate(request, user=self.mock_user)

        self.view.get(request)

        mock_serializer.assert_called_once_with(self.mock_user)

    @patch("core.views.users.UserSerializer")
    def test_givenAuthenticatedUser_whenGet_thenShouldReturn200(self, mock_serializer):
        request = self.factory.get("/profile/")
        request.user = self.mock_user
        force_authenticate(request, user=self.mock_user)

        response = self.view.get(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestPresenceIndicatorView(unittest.TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = PresenceIndicatorView()
        self.mock_user = MagicMock()
        self.mock_user.id = TEST_USER_ID

    @patch("core.views.users.UserService")
    def test_givenAuthenticatedUser_whenGet_thenShouldCallServiceGetPresenceData(
        self, mock_service
    ):
        request = self.factory.get("/presence/")
        request.user = self.mock_user
        force_authenticate(request, user=self.mock_user)

        self.view.get(request)

        mock_service.getPresenceData.assert_called_once_with(TEST_USER_ID)

    @patch("core.views.users.UserService")
    def test_givenServiceReturnsData_whenGet_thenShouldReturn200AndData(
        self, mock_service
    ):
        request = self.factory.get("/presence/")
        request.user = self.mock_user
        force_authenticate(request, user=self.mock_user)

        mock_service.getPresenceData.return_value = TEST_PRESENCE_DATA

        response = self.view.get(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, TEST_PRESENCE_DATA)


if __name__ == "__main__":
    unittest.main()
