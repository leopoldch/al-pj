from rest_framework import serializers
from ..models.album import Album
from ..models.photo import Photo


class AlbumSerializer(serializers.ModelSerializer):
    nb_photos = serializers.SerializerMethodField()

    class Meta:
        model = Album
        fields = [
            "id",
            "title",
            "description",
            "created_at",
            "updated_at",
            "cover_image",
            "nb_photos",
        ]
        read_only_fields = ["created_at", "updated_at"]

    def get_nb_photos(self, album):
        return Photo.objects.filter(album=album).count()

    def create(self, validated_data):
        request = self.context.get("request")
        if request and not request.user.is_authenticated:
            return None
        return super().create(validated_data)


