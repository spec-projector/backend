from random import randint

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from apps.core.models.mixins import Timestamps

CODE_EXPIRE_AFTER_MIN = 10
CODE_LENGTH = 6


def default_code():
    """Generate default code from digits."""
    return str(randint(100000, 999999))  # noqa: WPS432 S311


def default_expired_at():
    """Sets expiration ahead for n minutes."""
    return timezone.now() + timezone.timedelta(minutes=CODE_EXPIRE_AFTER_MIN)


class ResetPasswordRequest(Timestamps):
    """Reset password request model."""

    class Meta:
        verbose_name = _("VN__RESET_PASSWORD_REQUEST")
        verbose_name_plural = _("VN__RESET_PASSWORD_REQUESTS")
        ordering = ("-created_at",)

    code = models.CharField(
        max_length=CODE_LENGTH,
        db_index=True,
        default=default_code,
        verbose_name=_("VN__CODE"),
        help_text=_("HT__CODE"),
    )

    expired_at = models.DateTimeField(
        default=default_expired_at,
        verbose_name=_("VN__EXPIRED_AT"),
        help_text=_("HT__EXPIRED_AT"),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        models.CASCADE,
        verbose_name=_("VN__USER"),
        help_text=_("HT__USER"),
    )

    def __str__(self):
        """Object present."""
        return self.code
