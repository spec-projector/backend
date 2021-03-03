from django.db import models
from django.utils.translation import gettext_lazy as _


class EmailMessageStatus(models.TextChoices):
    """Email status choices."""

    CREATED = "created", _("CH__CREATED")  # noqa: WPS115
    READY = "ready", _("CH__READY")  # noqa: WPS115
    SENDING = "sending", _("CH__SENDING")  # noqa: WPS115
    SENT = "sent", _("CH__SENT")  # noqa: WPS115
    ERROR = "error", _("CH__ERROR")  # noqa: WPS115
