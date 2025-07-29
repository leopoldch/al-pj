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
    class Meta:
        model = Album
        fields = [
            "id",
            "title",
            "description",
            "created_at",
            "updated_at",
            "cover_image",
        ]
        read_only_fields = ["created_at", "updated_at"]

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
        album_id = self.context.get("album_id")
        if request and not request.user.is_authenticated:
            return None
        if not album_id:
            raise serializers.ValidationError("Album ID is required.")
        validated_data["album_id"] = album_id
        return super().create(validated_data)
