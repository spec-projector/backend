from django.db import models

from apps.billing.models import Tariff
from apps.core.admin.api import BaseAutocompleteView


class BillingTariffAutocompleteView(BaseAutocompleteView):
    """Billing tariff autocomplete view."""

    model = Tariff

    def get_queryset(self) -> models.QuerySet:
        """Get queryset."""
        queryset = super().get_queryset()

        return queryset.filter(is_active=True)
