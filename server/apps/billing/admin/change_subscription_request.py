from django.contrib import admin

from apps.billing.models import ChangeSubscriptionRequest
from apps.core.admin.base import BaseModelAdmin


@admin.register(ChangeSubscriptionRequest)
class ChangeSubscriptionRequestAdmin(BaseModelAdmin):
    """Change subscription request admin."""

    list_display = ("user", "tariff", "created_at", "is_active")
    list_filter = ("tariff",)
    search_fields = ("user__email",)
    fields = (
        "hash",
        "created_at",
        "is_active",
        "user",
        "from_subscription",
        "to_subscription",
        "tariff",
    )
    readonly_fields = ("hash", "created_at")
    ordering = ("-created_at",)
