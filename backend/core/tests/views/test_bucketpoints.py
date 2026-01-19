import unittest
from unittest.mock import MagicMock, patch
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate
from core.views.bucketpoints import BucketPointView
from rest_framework.exceptions import ValidationError, NotFound

TEST_USER_ID = 1
TEST_BUCKETPOINT_ID = 10
TEST_BUCKETPOINT_TITLE = "Saut en parachute"
TEST_BUCKETPOINT_DATA = {"title": TEST_BUCKETPOINT_TITLE, "completed": False}
TEST_RETURNED_DATA = {
    "id": TEST_BUCKETPOINT_ID,
    "title": TEST_BUCKETPOINT_TITLE,
    "completed": False,
}


class TestBucketPointView(unittest.TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = BucketPointView()
        self.mock_user = MagicMock()
        self.mock_user.id = TEST_USER_ID

    @patch("core.views.bucketpoints.BucketPointService")
    def test_givenAuthenticatedUser_whenGet_thenShouldCallServiceGetAll(
        self, mock_service
    ):
        request = self.factory.get("/bucketpoints/")
        force_authenticate(request, user=self.mock_user)
        self.view.request = request
        self.view.format_kwarg = None

        self.view.get(request)

        mock_service.get_all.assert_called_once()

    @patch("core.views.bucketpoints.BucketPointService")
    def test_givenServiceReturnsData_whenGet_thenShouldReturn200(self, mock_service):
        request = self.factory.get("/bucketpoints/")
        force_authenticate(request, user=self.mock_user)
        self.view.request = request
        self.view.format_kwarg = None
        mock_service.get_all.return_value = [TEST_RETURNED_DATA]

        response = self.view.get(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch("core.views.bucketpoints.BucketPointService")
    def test_givenServiceReturnsData_whenGet_thenShouldReturnCorrectData(
        self, mock_service
    ):
        request = self.factory.get("/bucketpoints/")
        force_authenticate(request, user=self.mock_user)
        self.view.request = request
        self.view.format_kwarg = None
        mock_service.get_all.return_value = [TEST_RETURNED_DATA]

        response = self.view.get(request)

        self.assertEqual(response.data, [TEST_RETURNED_DATA])

    @patch("core.views.bucketpoints.BucketPointService")
    def test_givenValidData_whenPost_thenShouldCallServiceCreate(self, mock_service):
        request = self.factory.post("/bucketpoints/", TEST_BUCKETPOINT_DATA)
        request.data = TEST_BUCKETPOINT_DATA
        force_authenticate(request, user=self.mock_user)
        self.view.request = request
        self.view.format_kwarg = None

        self.view.post(request)

        mock_service.create.assert_called_once_with(
            data=TEST_BUCKETPOINT_DATA, context={"request": request}
        )

    @patch("core.views.bucketpoints.BucketPointService")
    def test_givenValidData_whenPost_thenShouldReturn201(self, mock_service):
        request = self.factory.post("/bucketpoints/", TEST_BUCKETPOINT_DATA)
        request.data = TEST_BUCKETPOINT_DATA
        force_authenticate(request, user=self.mock_user)
        self.view.request = request
        self.view.format_kwarg = None
        mock_service.create.return_value = TEST_RETURNED_DATA

        response = self.view.post(request)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @patch("core.views.bucketpoints.BucketPointService")
    def test_givenValidData_whenPost_thenShouldReturnCreatedData(self, mock_service):
        request = self.factory.post("/bucketpoints/", TEST_BUCKETPOINT_DATA)
        request.data = TEST_BUCKETPOINT_DATA
        force_authenticate(request, user=self.mock_user)
        self.view.request = request
        self.view.format_kwarg = None
        mock_service.create.return_value = TEST_RETURNED_DATA

        response = self.view.post(request)

        self.assertEqual(response.data, TEST_RETURNED_DATA)

    @patch("core.views.bucketpoints.BucketPointService")
    def test_givenServiceRaisesValidationError_whenPost_thenShouldRaiseValidationError(
        self, mock_service
    ):
        request = self.factory.post("/bucketpoints/", TEST_BUCKETPOINT_DATA)
        request.data = TEST_BUCKETPOINT_DATA
        force_authenticate(request, user=self.mock_user)
        self.view.request = request
        self.view.format_kwarg = None
        mock_service.create.side_effect = ValidationError("Invalid data")

        with self.assertRaises(ValidationError):
            self.view.post(request)

    @patch("core.views.bucketpoints.BucketPointService")
    def test_givenValidDataAndId_whenPut_thenShouldCallServiceUpdate(
        self, mock_service
    ):
        request = self.factory.put(
            f"/bucketpoints/{TEST_BUCKETPOINT_ID}/", TEST_BUCKETPOINT_DATA
        )
        request.data = TEST_BUCKETPOINT_DATA
        force_authenticate(request, user=self.mock_user)
        self.view.request = request
        self.view.format_kwarg = None
        self.view.kwargs = {"pk": TEST_BUCKETPOINT_ID}

        self.view.put(request, pk=TEST_BUCKETPOINT_ID)

        mock_service.update.assert_called_once_with(
            pk=TEST_BUCKETPOINT_ID, data=TEST_BUCKETPOINT_DATA
        )

    @patch("core.views.bucketpoints.BucketPointService")
    def test_givenValidDataAndId_whenPut_thenShouldReturn200(self, mock_service):
        request = self.factory.put(
            f"/bucketpoints/{TEST_BUCKETPOINT_ID}/", TEST_BUCKETPOINT_DATA
        )
        request.data = TEST_BUCKETPOINT_DATA
        force_authenticate(request, user=self.mock_user)
        self.view.request = request
        self.view.format_kwarg = None
        self.view.kwargs = {"pk": TEST_BUCKETPOINT_ID}
        mock_service.update.return_value = TEST_RETURNED_DATA

        response = self.view.put(request, pk=TEST_BUCKETPOINT_ID)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch("core.views.bucketpoints.BucketPointService")
    def test_givenValidDataAndId_whenPut_thenShouldReturnUpdatedData(
        self, mock_service
    ):
        request = self.factory.put(
            f"/bucketpoints/{TEST_BUCKETPOINT_ID}/", TEST_BUCKETPOINT_DATA
        )
        request.data = TEST_BUCKETPOINT_DATA
        force_authenticate(request, user=self.mock_user)
        self.view.request = request
        self.view.format_kwarg = None
        self.view.kwargs = {"pk": TEST_BUCKETPOINT_ID}
        mock_service.update.return_value = TEST_RETURNED_DATA

        response = self.view.put(request, pk=TEST_BUCKETPOINT_ID)

        self.assertEqual(response.data, TEST_RETURNED_DATA)

    @patch("core.views.bucketpoints.BucketPointService")
    def test_givenServiceRaisesNotFound_whenPut_thenShouldRaiseNotFound(
        self, mock_service
    ):
        request = self.factory.put(
            f"/bucketpoints/{TEST_BUCKETPOINT_ID}/", TEST_BUCKETPOINT_DATA
        )
        request.data = TEST_BUCKETPOINT_DATA
        force_authenticate(request, user=self.mock_user)
        self.view.request = request
        self.view.format_kwarg = None
        self.view.kwargs = {"pk": TEST_BUCKETPOINT_ID}
        mock_service.update.side_effect = NotFound("Not found")

        with self.assertRaises(NotFound):
            self.view.put(request, pk=TEST_BUCKETPOINT_ID)

    @patch("core.views.bucketpoints.BucketPointService")
    def test_givenValidId_whenDelete_thenShouldCallServiceDelete(self, mock_service):
        request = self.factory.delete(f"/bucketpoints/{TEST_BUCKETPOINT_ID}/")
        force_authenticate(request, user=self.mock_user)
        self.view.request = request
        self.view.format_kwarg = None
        self.view.kwargs = {"pk": TEST_BUCKETPOINT_ID}

        self.view.delete(request, pk=TEST_BUCKETPOINT_ID)

        mock_service.delete.assert_called_once_with(pk=TEST_BUCKETPOINT_ID)

    @patch("core.views.bucketpoints.BucketPointService")
    def test_givenValidId_whenDelete_thenShouldReturn204(self, mock_service):
        request = self.factory.delete(f"/bucketpoints/{TEST_BUCKETPOINT_ID}/")
        force_authenticate(request, user=self.mock_user)
        self.view.request = request
        self.view.format_kwarg = None
        self.view.kwargs = {"pk": TEST_BUCKETPOINT_ID}

        response = self.view.delete(request, pk=TEST_BUCKETPOINT_ID)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


if __name__ == "__main__":
    unittest.main()
