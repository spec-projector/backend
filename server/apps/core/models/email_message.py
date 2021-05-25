from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel
from apps.core.models.enums.email_status import EmailMessageStatus
from apps.core.models.mixins import Timestamps


class EmailMessage(Timestamps, BaseModel):
    """Email message model."""

    class Meta:
        """Meta."""

        verbose_name = _("VN__EMAIL_MESSAGE")
        verbose_name_plural = _("VN__EMAIL_MESSAGES")

    status = models.CharField(
        max_length=50,  # noqa: WPS432
        choices=EmailMessageStatus.choices,
        default=EmailMessageStatus.CREATED,
        verbose_name=_("VN__EMAIL_MESSAGE_STATUS"),
        help_text=_("HT__EMAIL_MESSAGE_STATUS"),
        db_index=True,
    )
    subject = models.CharField(
        max_length=255,  # noqa: WPS432
        verbose_name=_("VN__EMAIL_MESSAGE_SUBJECT"),
        help_text=_("HT__EMAIL_MESSAGE_SUBJECT"),
    )
    to = models.EmailField(
        verbose_name=_("VN__EMAIL_MESSAGE_TO"),
        help_text=_("HT__EMAIL_MESSAGE_TO"),
    )
    html = models.TextField(default=None)
    sender = models.EmailField(
        blank=True,
        verbose_name=_("VN__EMAIL_MESSAGE_SENDER"),
        help_text=_("HT__EMAIL_MESSAGE_SENDER"),
    )
    sent_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name=_("VN__EMAIL_MESSAGE_SENT_AT"),
        help_text=_("HT__EMAIL_MESSAGE_SENT_AT"),
    )
    status_info = models.TextField(
        blank=True,
        verbose_name=_("VN__EMAIL_MESSAGE_STATUS_INFO"),
        help_text=_("HT__EMAIL_MESSAGE_STATUS_INFO"),
    )

    def __str__(self):
        """Object representation."""
        return "{0} {1:%d.%m.%Y %H:%M:%S} [{2}]".format(  # noqa: WPS323
            self.to,
            self.created_at,
            self.status,
        )
