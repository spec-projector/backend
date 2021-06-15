from django.conf import settings
from django.db import models
from django.utils.baseconv import BASE64_ALPHABET
from django.utils.crypto import get_random_string
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel

MAX_NAME_LENGTH = 256
MAX_TOKEN_KEY_LENGTH = 64


class UserAccessToken(BaseModel):
    """User access token model."""

    class Meta:
        verbose_name = _("VN__USER_ACCESS_TOKEN")
        verbose_name_plural = _("VN__USER_ACCESS_TOKENS")

    name = models.CharField(
        max_length=MAX_NAME_LENGTH,
        verbose_name=_("VN__NAME"),
        help_text=_("HT__NAME"),
    )
    key = models.CharField(
        max_length=MAX_TOKEN_KEY_LENGTH,
        verbose_name=_("VN__KEY"),
        help_text=_("HT__KEY"),
        db_index=True,
        unique=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("VN__CREATED_AT"),
        help_text=_("HT__CREATED_AT"),
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        models.CASCADE,
        verbose_name=_("VN__USER"),
        help_text=_("HT__USER"),
        related_name="access_tokens",
    )

    def __str__(self):
        """String present object."""
        return self.name

    def save(self, *args, **kwargs) -> None:
        """Save object."""
        if not self.key:
            self.key = get_random_string(  # noqa: WPS601
                length=MAX_TOKEN_KEY_LENGTH,
                allowed_chars=BASE64_ALPHABET,
            )

        super().save(*args, **kwargs)
