import typing as ty

from django.contrib import admin
from django.urls import URLPattern, path

from apps.billing.admin.api.views import BillingTariffAutocompleteView
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

    def get_urls(self) -> ty.List[URLPattern]:
        """Get admin urls."""
        urls = super().get_urls()
        return [
            path(
                "autocomplete/",
                BillingTariffAutocompleteView.as_view(),
                name="billing_tariff_autocomplete",
            ),
            *urls,
        ]
