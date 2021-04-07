from django.db import models
from django.utils.translation import gettext_lazy as _


class SubscriptionStatus(models.TextChoices):
    """Subscription status."""

    ACTIVE = "ACTIVE", _("CH__ACTIVE")  # noqa: WPS115
    PAST_DUE = "PAST_DUE", _("CH__PAST_DUE")  # noqa: WPS115
    CANCELED = "CANCELED", _("CH__CANCELED")  # noqa: WPS115
    REJECTED = "REJECTED", _("CH__REJECTED")  # noqa: WPS115
    EXPIRED = "EXPIRED", _("CH__EXPIRED")  # noqa: WPS115
