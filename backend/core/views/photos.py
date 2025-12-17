from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from ..models import Album, Photo
from ..serializers import (
    PhotoSerializer,
)
from core.services import photo_repository

class PhotoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, album_id):
        # !! must have the designated album in the request (and be valid)
        # get only one photo or all photos of a designated album ?
        # does that even make sense to get only one photo ?
        if not request.user or not request.user.is_authenticated:
            return Response(
                {"detail": "Authentication required."},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        photos = Photo.objects.filter(album_id=album_id)
        photos = PhotoSerializer(photos, many=True).data
        return Response(
            {"photos": photos, "album_id": album_id},
            status=status.HTTP_200_OK,
        )

    def delete(self, request, album_id):
        pass

    def post(self, request, album_id):
        if not request.user or not request.user.is_authenticated:
            return Response(
                {"detail": "Authentication required."},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        try:
            album = Album.objects.get(pk=album_id)
            data = request.data.copy()
            if "image" in request.FILES and request.FILES["image"]:
                link = photo_repository.save_within_folder(
                    request.FILES["image"], folder_album_id=album_id
                )
                data["image_url"] = link
            data["album"] = album_id

            serializer = PhotoSerializer(
                data=data, context={"request": request, "album": album}
            )

            if serializer.is_valid():
                serializer.save(album=album)
                # TODO: Notify other users via websocket
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Album.DoesNotExist:
            return Response(
                {"detail": "Album not found."}, status=status.HTTP_404_NOT_FOUND
            )
