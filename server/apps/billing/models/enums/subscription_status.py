from django.db import models
from django.utils.translation import gettext_lazy as _


class SubscriptionStatus(models.TextChoices):
    """Subscription status."""

    CONFIRMING = "CONFIRMING", _("CH__CONFIRMING")  # noqa: WPS115
    ACTIVE = "ACTIVE", _("CH__ACTIVE")  # noqa: WPS115
    CANCELED = "CANCELED", _("CH__CANCELED")  # noqa: WPS115
    OPTION = "OPTION", _("CH__OPTION")  # noqa: WPS115
    EXPIRED = "EXPIRED", _("CH__EXPIRED")  # noqa: WPS115
