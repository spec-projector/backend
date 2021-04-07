from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.billing.models import Tariff
from apps.billing.models.enums import SubscriptionStatus
from apps.core.models.helpers.enums import max_enum_len

MAX_HASH_LENGTH = 128


class Subscription(models.Model):
    """Subscription model."""

    class Meta:
        verbose_name = _("VN__SUBSCRIPTION")
        verbose_name_plural = _("VN__SUBSCRIPTION")
        unique_together = ("user", "hash")

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("VN__CREATED"),
        help_text=_("HT__CREATED"),
    )

    active_until = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("VN__ACTIVE_UNTIL"),
        help_text=_("HT__ACTIVE_UNTIL"),
    )

    hash = models.CharField(
        max_length=MAX_HASH_LENGTH,
        verbose_name=_("VN__HASH"),
        help_text=_("HT__SUBSCRIPTION_HASH"),
        db_index=True,
    )

    status = models.CharField(
        choices=SubscriptionStatus.choices,
        max_length=max_enum_len(SubscriptionStatus),
        verbose_name=_("VN__STATUS"),
        help_text=_("HT__STATUS"),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        models.CASCADE,
        verbose_name=_("VN__USER"),
        help_text=_("HT__USER"),
        related_name="subscriptions",
    )

    tariff = models.ForeignKey(
        Tariff,
        models.SET_NULL,
        null=True,
        verbose_name=_("VN__TARIFF"),
        help_text=_("HT__TARIFF"),
    )

    def __str__(self):
        """Object present."""
        return "{0}: {1} [{2}]".format(self.user, self.tariff, self.created)
