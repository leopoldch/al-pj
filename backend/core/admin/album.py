from django.contrib import admin
from ..models import Album

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

admin.site.register(Album, AlbumAdmin)
