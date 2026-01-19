from rest_framework import serializers
from ..models.bucketpoint import BucketPoint


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
