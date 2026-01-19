from rest_framework import serializers
from ..models.message import Message
from .user import UserSerializer


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
