import uuid

from django.conf import settings
from django.db import models
from django.utils.baseconv import BASE64_ALPHABET
from django.utils.crypto import get_random_string
from django.utils.translation import gettext_lazy as _
from jnt_django_toolbox.models.fields import BitField

from apps.core.models import BaseModel
from apps.core.models.mixins import Timestamps
from apps.media.models.fields import ImageField
from apps.projects.models.enums import ProjectMemberRole, ProjectPermission
from apps.projects.models.project_member import ProjectMember


def get_new_id():
    """Generate new Id for project."""
    old_ids = list(Project.objects.values_list("id", flat=True))
    uid = get_random_string(8, BASE64_ALPHABET)

    while uid in old_ids:
        uid = get_random_string(8, BASE64_ALPHABET)

    return uid


class Project(Timestamps, BaseModel):
    """Project model."""

    class Meta:
        verbose_name = _("VN__PROJECT")
        verbose_name_plural = _("VN__PROJECTS")
        ordering = ("-created_at",)

    id = models.CharField(  # noqa: WPS125
        primary_key=True,
        default=get_new_id,
        editable=False,
        max_length=10,
        unique=True,
    )

    is_public = models.BooleanField(
        default=False,
        verbose_name=_("VN__IS_PUBLIC"),
        help_text=_("HT__IS_PUBLIC"),
    )

    title = models.CharField(
        max_length=255,  # noqa: WPS432
        verbose_name=_("VN__TITLE"),
        help_text=_("HT__TITLE"),
    )

    description = models.TextField(
        verbose_name=_("VN__DESCRIPTION"),
        help_text=_("HT__DESCRIPTION"),
    )

    db_name = models.CharField(  # noqa: WPS601
        max_length=50,  # noqa: WPS432
        verbose_name=_("VN__DB_NAME"),
        help_text=_("HT__DB_NAME"),
        blank=True,
    )
    emblem = ImageField(
        verbose_name=_("VN__EMBLEM"),
        help_text=_("HT__EMBLEM"),
    )
    public_permissions = BitField(
        flags=ProjectPermission.choices,
        default=0,
        verbose_name=_("VN__PUBLIC_PROJECT_PERMISSIONS"),
        help_text=_("HT__PUBLIC_PROJECT_PERMISSIONS"),
    )
    public_role = models.CharField(
        max_length=32,  # noqa: WPS432
        choices=ProjectMemberRole.choices,
        default=ProjectMemberRole.VIEWER,
        verbose_name=_("VN__PUBLIC_ROLE"),
        help_text=_("HT__PUBLIC_ROLE"),
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        models.CASCADE,
        null=True,
        verbose_name=_("VN__OWNER"),
        help_text=_("HT__OWNER"),
    )

    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through=ProjectMember,
        related_name="projects",
    )

    def __str__(self):
        """Text representation."""
        return self.title

    def save(self, *args, **kwargs):
        """Save object."""
        if not self.db_name:
            self.db_name = "f{0}".format(uuid.uuid4())  # noqa: WPS601

        super().save(*args, **kwargs)
