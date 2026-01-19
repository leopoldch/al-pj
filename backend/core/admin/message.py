from django.contrib import admin
from ..models import Message


class MessageAdmin(admin.ModelAdmin):
    list_display = ("user", "message", "created_at")
    search_fields = ("name", "email")
    list_filter = ("created_at",)
    ordering = ("-created_at",)


admin.site.register(Message, MessageAdmin)
