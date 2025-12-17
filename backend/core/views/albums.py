from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from ..models import Album
from ..serializers import (
    AlbumSerializer,
)
from core.services import photo_repository

class AlbumView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not request.user or not request.user.is_authenticated:
            return Response(
                {"detail": "Authentication required."},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        albums = Album.objects.all()
        serializer = AlbumSerializer(albums, many=True)
        return Response(serializer.data)

    def post(self, request):
        if not request.user or not request.user.is_authenticated:
            return Response(
                {"detail": "Authentication required."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        data = request.data.copy()
        if "image" in request.FILES and request.FILES["image"]:
            link = photo_repository.save(request.FILES["image"])
            data["cover_image"] = link

        serializer = AlbumSerializer(data=data)
        if serializer.is_valid():
            _ = serializer.save()
            # TODO: Use websockets to notify other users about the new album
            # For now we can use invalidate usequeries but this is not optimal
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, album_id):
        if not request.user or not request.user.is_authenticated:
            return Response(
                {"detail": "Authentication required."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        try:
            album = Album.objects.get(pk=album_id)
            data = request.data.copy()
            if "image" in request.FILES and request.FILES["image"]:
                if album.cover_image and album.cover_image != "":
                    photo_repository.delete_from_cloud(album.cover_image)
                link = photo_repository.save(request.FILES["image"])
                data["cover_image"] = link
            serializer = AlbumSerializer(album, data=data, partial=True)
            if serializer.is_valid():
                # updated_album = serializer.save()
                _ = serializer.save()
                # Notify other users about the update with websocket
                # TODO: Implement websocket notification
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Album.DoesNotExist:
            return Response(
                {"detail": "Album not found."}, status=status.HTTP_404_NOT_FOUND
            )

    def delete(self, request):
        # TODO: Implement delete album functionality
        # maybe delete all photos in the album too ?
        pass