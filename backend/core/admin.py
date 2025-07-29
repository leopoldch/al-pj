from django.contrib import admin
from .models import Message, BucketPoint, Album, Photo


class MessageAdmin(admin.ModelAdmin):
    list_display = ("user", "message", "created_at")
    search_fields = ("name", "email")
    list_filter = ("created_at",)
    ordering = ("-created_at",)


class BucketPointAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "completed", "created_at")
    search_fields = ("title",)
    list_filter = ("completed", "created_at")
    ordering = ("-created_at",)


class AlbumAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "description",
        "created_at",
        "updated_at",
        "cover_image",
    )
    search_fields = ("title", "created_at", "updated_at")
    list_filter = ("created_at", "updated_at")
    ordering = ("-created_at",)


class PhotoAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "album",
        "image_url",
        "caption",
        "created_at",
        "updated_at",
        "location",
    )
    search_fields = ("title", "album", "created_at", "updated_at", "location")
    list_filter = ("created_at", "updated_at")
    ordering = ("-created_at",)


admin.site.register(Message, MessageAdmin)
admin.site.register(BucketPoint, BucketPointAdmin)
admin.site.register(Album, AlbumAdmin)
admin.site.register(Photo, PhotoAdmin)
