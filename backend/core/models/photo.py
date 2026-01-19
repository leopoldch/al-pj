from django.db import models
from .album import Album


class Photo(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name="photos")
    image_url = models.URLField(max_length=200)
    caption = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    location = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Photo in {self.album.title} - {self.caption or 'No Caption'}"
