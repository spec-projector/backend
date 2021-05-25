from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.billing.models import Subscription, Tariff
from apps.core.models import BaseModel

MAX_HASH_LENGTH = 128


class ChangeSubscriptionRequest(BaseModel):
    """Change subscription model."""

    class Meta:
        verbose_name = _("VN__CHANGE_SUBSCRIPTION_REQUEST")
        verbose_name_plural = _("VN__CHANGE_SUBSCRIPTION_REQUEST")
        constraints = [
            models.UniqueConstraint(
                fields=("user", "hash"),
                name="%(app_label)s_%(class)s_unique",  # noqa: WPS323
            ),
        ]

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("VN__CREATED"),
        help_text=_("HT__CREATED"),
    )

    hash = models.CharField(
        max_length=MAX_HASH_LENGTH,
        verbose_name=_("VN__HASH"),
        help_text=_("HT__SUBSCRIPTION_HASH"),
        db_index=True,
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name=_("VN__IS_ACTIVE"),
        help_text=_("HT__IS_ACTIVE"),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        models.CASCADE,
        verbose_name=_("VN__USER"),
        help_text=_("HT__USER"),
        related_name="change_subscriptions_requests",
    )

    tariff = models.ForeignKey(
        Tariff,
        models.SET_NULL,
        null=True,
        verbose_name=_("VN__TARIFF"),
        help_text=_("HT__TARIFF"),
    )

    from_subscription = models.ForeignKey(
        Subscription,
        models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("VN__FROM_SUBSCRIPTION"),
        help_text=_("HT__FROM_SUBSCRIPTION"),
        related_name="+",
    )

    to_subscription = models.ForeignKey(
        Subscription,
        models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("VN__TO_SUBSCRIPTION"),
        help_text=_("HT__TO_SUBSCRIPTION"),
        related_name="+",
    )

    def __str__(self):
        """Object present."""
        return "{0}: {1} [{2}]".format(self.user, self.tariff, self.created_at)

    def clean(self):
        """Validate instance."""
        same_subscriptions = (
            self.from_subscription
            and self.from_subscription == self.to_subscription
        )
        if same_subscriptions:
            raise ValidationError(_("MSG__CHANGE_SUBSCRIPTION_REQUEST_SAME"))
