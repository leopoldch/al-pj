import unittest
from unittest.mock import MagicMock, patch
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate
from core.views.messages import MessageView
from rest_framework.exceptions import ValidationError, NotFound

TEST_USER_ID = 1
TEST_MESSAGE_ID = 55
TEST_MESSAGE_CONTENT = "Hello world"
TEST_MESSAGE_DATA = {"content": TEST_MESSAGE_CONTENT}
TEST_RETURNED_MESSAGE = {"id": TEST_MESSAGE_ID, "content": TEST_MESSAGE_CONTENT, "user_id": TEST_USER_ID}

class TestMessageView(unittest.TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = MessageView()
        self.mock_user = MagicMock()
        self.mock_user.id = TEST_USER_ID

    @patch("core.views.messages.MessageService")
    @patch("core.views.messages.MessageSerializer") # On mock aussi le serializer car getAll renvoie des objets bruts
    def test_givenAuthenticatedUser_whenGet_thenShouldCallServiceGetAll(self, mock_serializer, mock_service):
        request = self.factory.get("/messages/")
        force_authenticate(request, user=self.mock_user)
        self.view.request = request
        self.view.format_kwarg = None

        self.view.get(request)

        mock_service.getAll.assert_called_once()

    @patch("core.views.messages.MessageService")
    @patch("core.views.messages.MessageSerializer")
    def test_givenServiceReturnsData_whenGet_thenShouldReturn200(self, mock_serializer, mock_service):
        request = self.factory.get("/messages/")
        force_authenticate(request, user=self.mock_user)
        self.view.request = request
        self.view.format_kwarg = None
        
        mock_service.getAll.return_value = []
        
        response = self.view.get(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch("core.views.messages.MessageService")
    @patch("core.views.messages.MessageSerializer")
    def test_givenServiceReturnsData_whenGet_thenShouldReturnCorrectData(self, mock_serializer, mock_service):
        request = self.factory.get("/messages/")
        force_authenticate(request, user=self.mock_user)
        self.view.request = request
        self.view.format_kwarg = None
        
        mock_serializer_instance = MagicMock()
        mock_serializer_instance.data = [TEST_RETURNED_MESSAGE]
        mock_serializer.return_value = mock_serializer_instance
        
        response = self.view.get(request)

        self.assertEqual(response.data, [TEST_RETURNED_MESSAGE])

    @patch("core.views.messages.MessageService")
    def test_givenValidData_whenPost_thenShouldCallServiceCreateMessage(self, mock_service):
        request = self.factory.post("/messages/", TEST_MESSAGE_DATA)
        request.data = TEST_MESSAGE_DATA
        request.user = self.mock_user
        force_authenticate(request, user=self.mock_user)
        self.view.request = request
        self.view.format_kwarg = None

        self.view.post(request)

        mock_service.create_message.assert_called_once_with(
            sender=self.mock_user, 
            data=TEST_MESSAGE_DATA,
            request_context={"request": request}
        )

    @patch("core.views.messages.MessageService")
    def test_givenValidData_whenPost_thenShouldReturn201(self, mock_service):
        request = self.factory.post("/messages/", TEST_MESSAGE_DATA)
        request.data = TEST_MESSAGE_DATA
        request.user = self.mock_user
        force_authenticate(request, user=self.mock_user)
        self.view.request = request
        self.view.format_kwarg = None
        mock_service.create_message.return_value = TEST_RETURNED_MESSAGE

        response = self.view.post(request)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @patch("core.views.messages.MessageService")
    def test_givenValidData_whenPost_thenShouldReturnCreatedData(self, mock_service):
        request = self.factory.post("/messages/", TEST_MESSAGE_DATA)
        request.data = TEST_MESSAGE_DATA
        request.user = self.mock_user
        force_authenticate(request, user=self.mock_user)
        self.view.request = request
        self.view.format_kwarg = None
        mock_service.create_message.return_value = TEST_RETURNED_MESSAGE

        response = self.view.post(request)

        self.assertEqual(response.data, TEST_RETURNED_MESSAGE)


    @patch("core.views.messages.MessageService")
    def test_givenValidId_whenDelete_thenShouldCallServiceDelete(self, mock_service):
        request = self.factory.delete(f"/messages/{TEST_MESSAGE_ID}/")
        request.user = self.mock_user
        force_authenticate(request, user=self.mock_user)
        self.view.request = request
        self.view.format_kwarg = None
        self.view.kwargs = {"pk": TEST_MESSAGE_ID}

        self.view.delete(request, pk=TEST_MESSAGE_ID)

        mock_service.delete.assert_called_once_with(TEST_MESSAGE_ID, self.mock_user)

    @patch("core.views.messages.MessageService")
    def test_givenValidId_whenDelete_thenShouldReturn204(self, mock_service):
        request = self.factory.delete(f"/messages/{TEST_MESSAGE_ID}/")
        request.user = self.mock_user
        force_authenticate(request, user=self.mock_user)
        self.view.request = request
        self.view.format_kwarg = None
        self.view.kwargs = {"pk": TEST_MESSAGE_ID}

        response = self.view.delete(request, pk=TEST_MESSAGE_ID)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

if __name__ == "__main__":
    unittest.main()