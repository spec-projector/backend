from apps.core.admin.config.fields import BaseForeignConfigField


class TariffConfigField(BaseForeignConfigField):
    """Tariff config field."""

    def get_url(self) -> str:
        """Get autocomplete url."""
        return "/admin/billing/tariff/autocomplete/"
