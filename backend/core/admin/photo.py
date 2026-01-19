from django.contrib import admin
from ..models import Photo


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


admin.site.register(Photo, PhotoAdmin)
