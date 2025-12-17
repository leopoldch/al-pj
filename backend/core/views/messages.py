from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from ..serializers import (
    MessageSerializer
)
import os
from dotenv import load_dotenv, find_dotenv
from core.services import MessageService

load_dotenv(find_dotenv())


DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1", "t")

class MessageView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, _):
        messages = MessageService.getAll()
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

    def post(self, request):
        try:
            message_data = MessageService.create_message(
                sender=request.user, 
                data=request.data,
                request_context={"request": request}
            )
            return Response(message_data, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        if MessageService.delete(pk, request.user):
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)