from django.db import models
from django.utils.translation import gettext_lazy as _
from jnt_django_toolbox.models.fields import BitField

from apps.core.models.fields import MoneyField


class TariffFeatures(models.TextChoices):
    """Tariff features choices."""

    PROJECT_MEMBERS_ROLES = "PROJECT_MEMBERS_ROLES", _(  # noqa: WPS115
        "CH__PROJECT_MEMBERS_ROLES",
    )
    PRINT_CONTRACT = "PRINT_CONTRACT", _("CH__PRINT_CONTRACT")  # noqa: WPS115
    EXPORT_IMPORT = "EXPORT_IMPORT", _("CH__EXPORT_IMPORT")  # noqa: WPS115
    COMMUNITY_CHAT = "COMMUNITY_CHAT", _("CH__COMMUNITY_CHAT")  # noqa: WPS115
    SLACK_SUPPORT = "SLACK_SUPPORT", _("CH__SLACK_SUPPORT")  # noqa: WPS115
    EXCLUSIVE_SLACK_SUPPORT = "EXCLUSIVE_SLACK_SUPPORT", _(  # noqa: WPS115
        "CH__EXCLUSIVE_SLACK_SUPPORT",
    )


class Tariff(models.Model):
    """Tariff model."""

    class Meta:
        verbose_name = _("VN__TARIFF")
        verbose_name_plural = _("VN__TARIFFS")
        ordering = ("order",)

    order = models.PositiveSmallIntegerField(
        default=0,
        verbose_name=_("VN__ORDER"),
        help_text=_("HT__ORDER"),
    )
    code = models.CharField(
        max_length=64,  # noqa: WPS432
        verbose_name=_("VN__CODE"),
        help_text=_("HT__CODE"),
    )
    title = models.CharField(
        max_length=128,  # noqa: WPS432
        verbose_name=_("VN__TITLE"),
        help_text=_("HT__TITLE"),
    )
    teaser = models.TextField(
        verbose_name=_("VN__TEASER"),
        help_text=_("HT__TEASER"),
    )
    icon = models.CharField(
        max_length=512,  # noqa: WPS432
        blank=True,
        verbose_name=_("VN__ICON"),
        help_text=_("HT__ICON"),
    )
    price = MoneyField(
        default=0,
        verbose_name=_("VN__PRICE"),
        help_text=_("HT__PRICE"),
    )
    is_active = models.BooleanField(
        default=False,
        verbose_name=_("VN__IS_ACTIVE"),
        help_text=_("HT__IS_ACTIVE"),
    )
    features = BitField(
        flags=TariffFeatures.choices,
        default=0,
        verbose_name=_("VN__FEATURES"),
        help_text=_("HT__FEATURES"),
    )
    max_projects = models.PositiveIntegerField(
        default=0,
        verbose_name=_("VN__MAX_PROJECTS"),
        help_text=_("HT__MAX_PROJECTS"),
    )
    max_project_members = models.PositiveIntegerField(
        default=0,
        verbose_name=_("VN__MAX_PROJECT_MEMBERS"),
        help_text=_("HT__MAX_PROJECT_MEMBERS"),
    )

    def __str__(self):
        """Object present."""
        return self.title
