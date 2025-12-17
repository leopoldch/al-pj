from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from core.exceptions import ResourceNotFound, CloudUploadError, InsufficientRights
from django.core.exceptions import ObjectDoesNotExist

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        return response
    
    if isinstance(exc, (ResourceNotFound, ObjectDoesNotExist)):
        return Response(
            {"detail": "La ressource demandée est introuvable.", "code": "NOT_FOUND"},
            status=status.HTTP_404_NOT_FOUND
        )

    if isinstance(exc, InsufficientRights):
        return Response(
            {"detail": str(exc), "code": "FORBIDDEN"},
            status=status.HTTP_403_FORBIDDEN
        )
        
    if isinstance(exc, CloudUploadError):
        return Response(
            {"detail": "Erreur de communication avec le service de stockage.", "code": "CLOUD_ERROR"},
            status=status.HTTP_503_SERVICE_UNAVAILABLE
        )

    return None