from django.contrib import admin

from apps.billing.models import Subscription
from apps.core.admin.base import BaseModelAdmin


@admin.register(Subscription)
class SubscriptionAdmin(BaseModelAdmin):
    """Subscription admin."""

    list_display = ("user", "tariff", "created", "status")
    list_filter = ("tariff", "status")
    search_fields = ("user__email",)
    fields = ("hash", "created", "status", "active_until", "user", "tariff")
    readonly_fields = ("hash", "created", "active_until")
    ordering = ("-created",)
