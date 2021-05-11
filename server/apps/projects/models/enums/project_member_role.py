from django.db import models
from django.utils.translation import gettext_lazy as _


class ProjectMemberRole(models.TextChoices):
    """Project member role choices."""

    VIEWER = "VIEWER", _("CH__VIEWER")  # noqa: WPS115
    EDITOR = "EDITOR", _("CH__EDITOR")  # noqa: WPS115
