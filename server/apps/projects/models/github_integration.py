from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel

MAX_TOKEN_LENGTH = 128


class GitHubIntegration(BaseModel):
    """GitHub integration model."""

    class Meta:
        verbose_name = _("VN__GITHUB_INTEGRATION")
        verbose_name_plural = _("VN__GITHUB_INTERGRATIONS")

    token = models.CharField(
        verbose_name=_("VN__TOKEN"),
        help_text=_("HT__TOKEN"),
        max_length=MAX_TOKEN_LENGTH,
        blank=True,
        default="",
    )

    project = models.OneToOneField(
        "projects.Project",
        models.CASCADE,
        verbose_name=_("VN__PROJECT"),
        help_text=_("HT__PROJECT"),
        related_name="github_integration",
    )

    def __str__(self):
        """Returns object string representation."""
        return "GitHub integration #{0}".format(self.pk)
