from django.contrib import admin

from apps.billing.models import Tariff
from apps.core.admin.base import BaseModelAdmin


@admin.register(Tariff)
class TariffAdmin(BaseModelAdmin):
    """Tariff admin."""

    list_display = ("title", "code", "price", "is_active")
    list_filter = ("is_active",)
    search_fields = ("title", "code", "teaser", "=id")
    ordering = ("order",)
    fields = (
        "order",
        "code",
        "title",
        "teaser",
        "icon",
        "price",
        "is_active",
        "features",
        "max_projects",
        "max_project_members",
    )
