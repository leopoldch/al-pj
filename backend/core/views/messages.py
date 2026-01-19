from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from ..serializers import MessageSerializer
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

        message_data = MessageService.create_message(
            sender=request.user, data=request.data, request_context={"request": request}
        )
        return Response(message_data, status=status.HTTP_201_CREATED)

    def delete(self, request, pk):
        MessageService.delete(pk, request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)


from rest_framework.pagination import PageNumberPagination


class MessagePagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 100


class PaginatedMessageView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        messages = MessageService.getAll()
        paginator = MessagePagination()
        paginated_messages = paginator.paginate_queryset(messages, request)
        serializer = MessageSerializer(paginated_messages, many=True)
        return paginator.get_paginated_response(serializer.data)
