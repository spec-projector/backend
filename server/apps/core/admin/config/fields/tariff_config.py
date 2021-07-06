from apps.billing.models import Tariff
from apps.core.admin.config.fields import BaseForeignConfigField


class TariffConfigField(BaseForeignConfigField):
    """Tariff config field."""

    model = Tariff
    autocomplete_url = "/admin/billing/tariff/autocomplete/"
