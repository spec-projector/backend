# -*- coding: utf-8 -*-

from bitfield import BitField
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models.choises import Choices
from apps.core.models.mixins import Timestamps

PROJECT_MEMBER_ROLES = Choices(
    ("FRONTEND_DEVELOPER", _("CH__FRONTEND_DEVELOPER")),
    ("BACKEND_DEVELOPER", _("CH__BACKEND_DEVELOPER")),
    ("PROJECT_MANAGER", _("CH__PROJECT_MANAGER")),
    ("DESIGNER", _("CH__DESIGNER")),
    ("TESTER", _("CH__TESTER")),
    ("CUSTOMER", _("CH__CUSTOMER")),
)


class ProjectMember(Timestamps):
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

    roles = BitField(
        flags=PROJECT_MEMBER_ROLES,
        default=0,
    )

    def __str__(self):
        """Returns object string representation."""
        return "{0}: {1}".format(self.project, self.user)

    class Meta:
        verbose_name = _("VN__PROJECT_MEMBER")
        verbose_name_plural = _("VN__PROJECT_MEMBERS")
        unique_together = ("project", "user")
