from django.test import TestCase, RequestFactory
from rest_framework.views import APIView
from rest_framework import status
from core.exceptions.handler import custom_exception_handler
from core.exceptions import ResourceNotFound, InsufficientRights, CloudUploadError
from django.core.exceptions import ObjectDoesNotExist

class TestExceptionHandler(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.request = self.factory.get('/')

    def test_resource_not_found(self):
        exc = ResourceNotFound("Not found")
        response = custom_exception_handler(exc, {'request': self.request})
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['code'], 'NOT_FOUND')

    def test_object_does_not_exist(self):
        exc = ObjectDoesNotExist("Not found")
        response = custom_exception_handler(exc, {'request': self.request})
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['code'], 'NOT_FOUND')

    def test_insufficient_rights(self):
        exc = InsufficientRights("Forbidden")
        response = custom_exception_handler(exc, {'request': self.request})
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['code'], 'FORBIDDEN')

    def test_cloud_upload_error(self):
        exc = CloudUploadError("Cloud error")
        response = custom_exception_handler(exc, {'request': self.request})
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, status.HTTP_503_SERVICE_UNAVAILABLE)
        self.assertEqual(response.data['code'], 'CLOUD_ERROR')

    def test_unhandled_exception(self):
        exc = Exception("Unhandled")
        response = custom_exception_handler(exc, {'request': self.request})
        self.assertIsNone(response)
