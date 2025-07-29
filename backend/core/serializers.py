from rest_framework import serializers
from .models import Message, BucketPoint, Album, Photo
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "date_joined"]


class MessageSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    email = serializers.EmailField(source="user.email", read_only=True)
    name = serializers.CharField(
        source="user.get_full_name", read_only=True
    ) or serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = Message
        fields = ["id", "user", "name", "email", "message", "created_at", "status"]
        read_only_fields = ["user", "name", "email", "created_at", "status"]

    def create(self, validated_data):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            validated_data["user"] = request.user
        return super().create(validated_data)


class BucketPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = BucketPoint
        fields = ["id", "title", "description", "completed", "created_at"]
        read_only_fields = ["created_at"]

    def create(self, validated_data):
        request = self.context.get("request")
        if request and not request.user.is_authenticated:
            return None
        return super().create(validated_data)


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


class PhotoSerializer(serializers.ModelSerializer):
    album = AlbumSerializer(read_only=True)

    class Meta:
        model = Photo
        fields = [
            "id",
            "album",
            "image_url",
            "caption",
            "created_at",
            "updated_at",
            "location",
        ]
        read_only_fields = ["created_at", "updated_at"]


def create(self, validated_data):
    request = self.context.get("request")
    if request and not request.user.is_authenticated:
        return None
    album = self.context.get("album")
    if not album:
        raise serializers.ValidationError({"album": "Album manquant"})

    return Photo.objects.create(album=album, **validated_data)
