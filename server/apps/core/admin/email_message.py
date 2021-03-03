from django.contrib import admin

from apps.core.admin.base import BaseModelAdmin
from apps.core.models import EmailMessage


@admin.register(EmailMessage)
class EmailMessageAdmin(BaseModelAdmin):
    """Email messages admin."""

    list_display = ("created_at", "to", "status")
    search_fields = ("html", "to", "sender")
    list_filter = ("status",)
