from ..models import Album
from ..serializers import AlbumSerializer
from core.dependencies import photo_repository


class AlbumService:
    
    @staticmethod
    def getAll():
        albums = Album.objects.all()
        return albums
    
    @staticmethod
    def createAlbum(raw_data, file):
        data = raw_data.copy()
        if "image" in file and file["image"]:
            link = photo_repository.save(file["image"])
            data["cover_image"] = link

        serializer = AlbumSerializer(data=data)
        
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer.data

    @staticmethod
    def _replace_cover_image(data, album, file):
        if album.cover_image and album.cover_image != "":
            photo_repository.delete(album.cover_image)
            link = photo_repository.save(file["image"])
            data["cover_image"] = link
        return data

    @classmethod
    def modifyAlbum(cls, id, raw_data, file):
        data = raw_data.copy()
        album = Album.objects.get(pk=id)

        if "image" in file and file["image"]:
            data = cls._replace_cover_image(data, album, file)
            serializer = AlbumSerializer(album, data=data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            # TODO: Use websockets to notify other users about the new album
            return serializer.data
        return None