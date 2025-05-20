from rest_framework import serializers
from .models import Message, BucketPoint
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "date_joined"]


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ["id", "user", "name", "email", "message", "created_at", "status"]
        read_only_fields = ["user", "name", "email", "created_at", "status"]

    def create(self, validated_data):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            validated_data["user"] = request.user
            validated_data["name"] = request.user.username
            validated_data["email"] = request.user.email
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
