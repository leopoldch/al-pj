from django.contrib import admin
from .models import Message, BucketPoint

# Register your models here.


class MessageAdmin(admin.ModelAdmin):
    list_display = ("user", "name", "email", "message", "created_at")
    search_fields = ("name", "email")
    list_filter = ("created_at",)
    ordering = ("-created_at",)


class BucketPointAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "completed", "created_at")
    search_fields = ("title",)
    list_filter = ("completed", "created_at")
    ordering = ("-created_at",)


admin.site.register(Message, MessageAdmin)
admin.site.register(BucketPoint, BucketPointAdmin)
