from django.contrib import admin
from ..models import BucketPoint


class BucketPointAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "completed", "created_at")
    search_fields = ("title",)
    list_filter = ("completed", "created_at")
    ordering = ("-created_at",)


admin.site.register(BucketPoint, BucketPointAdmin)
