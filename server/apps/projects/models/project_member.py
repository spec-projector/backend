# -*- coding: utf-8 -*-

from bitfield import BitField
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models.mixins import Timestamps


class ProjectMemberRole(models.TextChoices):
    """Project member role choices."""

    FRONTEND_DEVELOPER = (  # noqa: WPS115
        "FRONTEND_DEVELOPER",
        _("CH__FRONTEND_DEVELOPER"),
    )
    BACKEND_DEVELOPER = (  # noqa: WPS115
        "BACKEND_DEVELOPER",
        _("CH__BACKEND_DEVELOPER"),
    )
    PROJECT_MANAGER = (  # noqa: WPS115
        "PROJECT_MANAGER",
        _("CH__PROJECT_MANAGER"),
    )
    DESIGNER = "DESIGNER", _("CH__DESIGNER")  # noqa: WPS115
    TESTER = "TESTER", _("CH__TESTER")  # noqa: WPS115
    CUSTOMER = "CUSTOMER", _("CH__CUSTOMER")  # noqa: WPS115


class ProjectMember(Timestamps):
    """Project member model."""

    project = models.ForeignKey(
        "projects.Project",
        models.CASCADE,
        verbose_name=_("VN__PROJECT"),
        help_text=_("HT__PROJECT"),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        models.CASCADE,
        verbose_name=_("VN__USER"),
        help_text=_("HT__USER"),
    )

    roles = BitField(flags=ProjectMemberRole.choices, default=0)

    def __str__(self):
        """Returns object string representation."""
        return "{0}: {1}".format(self.project, self.user)

    class Meta:
        verbose_name = _("VN__PROJECT_MEMBER")
        verbose_name_plural = _("VN__PROJECT_MEMBERS")
        unique_together = ("project", "user")
