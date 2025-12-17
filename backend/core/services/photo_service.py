from core.models import Album
from core.serializers import PhotoSerializer
from core.models import Photo
from core.dependencies import photo_repository


class PhotoService:

    @staticmethod
    def get_photos_by_album_id(album_id):
        photos = Photo.objects.filter(album_id=album_id)
        photos = PhotoSerializer(photos, many=True).data
        return photos
    
    @staticmethod
    def save_photo(album_id, request):
        data = request.data.copy()
        file = request.FILES
        album = Album.objects.get(pk=album_id)
        if "image" in file and file["image"]:
            link = photo_repository.save_within_folder(
                file["image"], folder_album_id=album_id
            )
            data["image_url"] = link
        data["album"] = album_id

        serializer = PhotoSerializer(
            data=data, context={"request": request, "album": album}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(album=album)
        return serializer.data