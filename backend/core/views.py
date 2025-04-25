from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Message
from .serializers import MessageSerializer
from .serializers import UserSerializer
from core.utils import send_formatted_mail
from django.contrib.auth.models import User


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


class MessageView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not request.user or not request.user.is_authenticated:
            return Response(
                {"detail": "Authentication required."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        messages = Message.objects
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

    def post(self, request):
        if not request.user or not request.user.is_authenticated:
            return Response(
                {"detail": "Authentication required."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        serializer = MessageSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()

            # get all the users except the one who sent the message
            users = User.objects.exclude(id=request.user.id)
            for user in users:
                send_formatted_mail(str(user.email), str(user.username))
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        if not request.user or not request.user.is_authenticated:
            return Response(
                {"detail": "Authentication required."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        try:
            message = Message.objects.get(pk=pk, user=request.user)
            if message.user != request.user:
                return Response(
                    {"detail": "You do not have permission to delete this message."},
                    status=status.HTTP_403_FORBIDDEN,
                )
            message.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Message.DoesNotExist:
            return Response(
                {"detail": "Message not found."}, status=status.HTTP_404_NOT_FOUND
            )
