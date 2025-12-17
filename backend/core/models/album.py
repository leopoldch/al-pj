from django.db import models

class Album(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    cover_image = models.URLField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.title