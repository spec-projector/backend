# -*- coding: utf-8 -*-

from django.conf import settings
from django.db import models
from django.utils.baseconv import BASE64_ALPHABET
from django.utils.crypto import get_random_string
from django.utils.translation import gettext_lazy as _

from apps.core.models.mixins import Timestamps
from apps.projects.models.project_member import ProjectMember


def get_new_id():
    """Generate new Id for project."""
    old_ids = list(Project.objects.values_list("id", flat=True))
    uid = get_random_string(8, BASE64_ALPHABET)

    while uid in old_ids:
        uid = get_random_string(8, BASE64_ALPHABET)

    return uid


class Project(Timestamps):
    """Project model."""

    class Meta:
        verbose_name = _("VN__PROJECT")
        verbose_name_plural = _("VN__PROJECTS")
        ordering = ("-created_at",)

    id = models.CharField(  # noqa: A003,WPS125
        primary_key=True,
        default=get_new_id,
        editable=False,
        max_length=10,
        unique=True,
    )

    public = models.BooleanField(default=False)

    title = models.CharField(
        max_length=255,  # noqa: WPS432
        verbose_name=_("VN__TITLE"),
        help_text=_("HT__TITLE"),
    )

    description = models.TextField(
        verbose_name=_("VN__DESCRIPTION"), help_text=_("HT__DESCRIPTION"),
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
