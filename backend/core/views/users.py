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
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class PresenceIndicatorView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = UserService.getPresenceData(request.user.id)
        return Response(data, status=status.HTTP_200_OK)
