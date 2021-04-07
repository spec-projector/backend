from django.utils.translation import gettext_lazy as _

from apps.core.services.errors import BaseInfrastructureError


class BaseSubscriptionError(BaseInfrastructureError):
    """Base subscription error."""


class InvalidTariffError(BaseSubscriptionError):
    """Invalid tariff error."""

    code = "invalid_tariff"
    message = _("MSG__INVALID_TARIFF")
