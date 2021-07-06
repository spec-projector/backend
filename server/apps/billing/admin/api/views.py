from django.contrib import admin
from django.db import models

from apps.billing.models import Tariff
from apps.core.admin.api import BaseAutocompleteView


class BillingTariffAutocompleteView(BaseAutocompleteView):
    """Billing tariff autocomplete view."""

    def get_model_admin(self) -> admin.ModelAdmin:
        """Get model admin for autocomplete view."""
        return admin.site._registry.get(Tariff)  # noqa: WPS437

    def get_queryset(self) -> models.QuerySet:
        """Get queryset."""
        queryset = super().get_queryset()

        return queryset.filter(is_active=True)
