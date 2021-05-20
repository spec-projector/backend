from django.contrib import admin

from apps.core.admin.base import BaseModelAdmin
from apps.media.models import File


@admin.register(File)
class FileAdmin(BaseModelAdmin):
    """File admin."""

    list_display = ("original_filename", "created_at", "owner")
    search_fields = ("original_filename", "=id")
    ordering = ("-created_at",)
    readonly_fields = ("owner", "created_at", "updated_at")

    def save_model(self, request, instance, form, change):
        """Save image model from admin."""
        if not instance.owner:
            instance.owner = request.user
        super().save_model(request, instance, form, change)
