from django.db import models
from django.contrib.auth.models import User


class Message(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="messages")
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return f"Message from {self.name} at {self.created_at}"


class BucketPoint(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Bridge(models.Model):
    
    nb_locks = models.IntegerField()
    last_modified = models.DateTimeField(auto_now=True)
    # other fields can be added as needed
    
    def __str__(self):
        return f"Bridge with {self.nb_locks} locks, last modified at {self.last_modified}"

class Lock(models.Model):
    
    bridge = models.ForeignKey(Bridge, on_delete=models.CASCADE, related_name='locks')
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='locks')
    lock_number = models.IntegerField()
    message = models.TextField(blank=True, null=True)
    
    # Coordinates for the lock
    x = models.FloatField()
    y = models.FloatField()
    
    def save(self, *args, **kwargs):
        if not self.lock_number:
            # Count existing locks for this bridge and user
            existing_count = Lock.objects.filter(bridge=self.bridge, user=self.user).count()
            self.lock_number = existing_count + 1
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Lock {self.lock_number} on Bridge with {self.bridge.nb_locks} locks"