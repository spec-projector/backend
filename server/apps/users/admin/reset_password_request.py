from django.contrib import admin

from apps.core.admin.base import BaseModelAdmin
from apps.users.models import ResetPasswordRequest


@admin.register(ResetPasswordRequest)
class ResetPasswordRequestAdmin(BaseModelAdmin):
    """Reset password request admin."""

    list_display = ("code", "user", "expired_at")
    search_fields = (
        "code",
        "user__email",
    )
