from core.services import PhotoService
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status


class PhotoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, _, album_id):        
        photos = PhotoService.get_photos_by_album_id(album_id)
        return Response(
            {"photos": photos, "album_id": album_id},
            status=status.HTTP_200_OK,
        )

    def delete(self, request, album_id):
        pass

    def post(self, request, album_id):
        PhotoService.save_photo(album_id, request)
        return Response(status=status.HTTP_201_CREATED)
