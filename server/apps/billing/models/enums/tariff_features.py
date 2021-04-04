from django.db import models
from django.utils.translation import gettext_lazy as _


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
