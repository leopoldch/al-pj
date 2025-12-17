from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from ..serializers import (
    UserSerializer,
)
from core.services import UserService


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not request.user or not request.user.is_authenticated:
            return Response(
                {"detail": "Authentication required."},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    
class PresenceIndicatorView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not request.user or not request.user.is_authenticated:
            return Response(
                {"detail": "Authentication required."},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        
        data = UserService.getPresenceData(request.user.id)
        return Response(data, 201)

        