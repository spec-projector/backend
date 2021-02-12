from django.db import models
from django.utils.translation import gettext_lazy as _
from jnt_django_toolbox.models.fields import EnumField

from apps.core.models.mixins import Timestamps
from apps.projects.services.projects.upload_assets import assets_upload_to


class ProjectAssetSource(models.TextChoices):
    """Project asset source."""

    FIGMA = "FIGMA", _("CH__FIGMA")  # noqa: WPS115


class ProjectAsset(Timestamps):
    """Project asset model."""

    class Meta:
        verbose_name = _("VN__PROJECT_ASSET")
        verbose_name_plural = _("VN__PROJECTS_ASSETS")
        ordering = ("-created_at",)

    source = EnumField(
        enum=ProjectAssetSource,
        default=ProjectAssetSource.FIGMA,
        verbose_name=_("VN__PROJECT_ASSET_SOURCE"),
        help_text=_("HT__PROJECT_ASSET_SOURCE"),
    )

    file = models.FileField(  # noqa: WPS110
        upload_to=assets_upload_to,
        max_length=256,  # noqa: WPS432
        blank=True,
        verbose_name=_("VN__FILE"),
        help_text=_("HT__FILE"),
    )
    project = models.ForeignKey(
        "projects.Project",
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_("VN__PROJECT"),
        help_text=_("HT__PROJECT"),
    )

    def __str__(self):
        """Object present."""
        return self.source
