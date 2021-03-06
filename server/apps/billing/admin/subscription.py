from django.contrib import admin

from apps.billing.models import Subscription
from apps.core.admin.base import BaseModelAdmin


@admin.register(Subscription)
class SubscriptionAdmin(BaseModelAdmin):
    """Subscription admin."""

    list_display = ("user", "tariff", "created_at", "status")
    list_filter = ("tariff", "status")
    search_fields = ("user__email",)
    fields = (
        "created_at",
        "status",
        "active_until",
        "user",
        "tariff",
        "merchant_id",
    )
    readonly_fields = ("created_at", "active_until")
    ordering = ("-created_at",)
