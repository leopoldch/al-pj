from django.db import models

class BucketPoint(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(null=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    