from core.services import AlbumService
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from ..serializers import (
    AlbumSerializer,
)


class AlbumView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, _):
        albums = AlbumService.getAll()
        serializer = AlbumSerializer(albums, many=True)
        return Response(serializer.data)

    def post(self, request):
        serialized_data = AlbumService.createAlbum(request.data, request.FILES)
        return Response(serialized_data, status=status.HTTP_201_CREATED)

    def put(self, request, album_id):
        serialized_data = AlbumService.modifyAlbum(
            album_id, request.data, request.FILES
        )
        return Response(serialized_data)

    def delete(self, request):
        # TODO: Implement delete album functionality
        # maybe delete all photos in the album too ?
        pass
