from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from jnt_django_toolbox.models.fields import BitField

from apps.core.models import BaseModel
from apps.core.models.mixins import Timestamps
from apps.projects.models.enums import ProjectMemberRole, ProjectPermission


class ProjectMember(Timestamps, BaseModel):
    """Project member model."""

    class Meta:
        verbose_name = _("VN__PROJECT_MEMBER")
        verbose_name_plural = _("VN__PROJECT_MEMBERS")
        unique_together = ("project", "user")

    role = models.CharField(
        max_length=28,  # noqa: WPS432
        choices=ProjectMemberRole.choices,
        default=ProjectMemberRole.VIEWER,
        verbose_name=_("VN__ROLE"),
        help_text=_("HT__ROLE"),
    )
    permissions = BitField(
        flags=ProjectPermission.choices,
        default=0,
        verbose_name=_("VN__PROJECT_PERMISSIONS"),
        help_text=_("HT__PROJECT_PERMISSIONS"),
    )

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

    def __str__(self):
        """Returns object string representation."""
        return "{0}: {1}".format(self.project, self.user)
