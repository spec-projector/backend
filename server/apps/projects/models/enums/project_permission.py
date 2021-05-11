from django.db import models
from django.utils.translation import gettext_lazy as _


class ProjectPermission(models.TextChoices):
    """Project permission."""

    EDIT_FEATURES = "EDIT_FEATURES", _("CH__EDIT_FEATURES")  # noqa: WPS115
    EDIT_FEATURE_WORKFLOW = (  # noqa: WPS115
        "EDIT_FEATURE_WORKFLOW",
        _("CH__EDIT_FEATURE_WORKFLOW"),
    )
    EDIT_FEATURE_STORY = (  # noqa: WPS115
        "EDIT_FEATURE_STORY",
        _("CH__EDIT_FEATURE_STORY"),
    )
    EDIT_FEATURE_FRAMES = (  # noqa: WPS115
        "EDIT_FEATURE_FRAMES",
        _("CH__EDIT_FEATURE_FRAMES"),
    )
    EDIT_FEATURE_RESOURCES = (  # noqa: WPS115
        "EDIT_FEATURE_RESOURCES",
        _("CH__EDIT_FEATURE_RESOURCES"),
    )
    EDIT_FEATURE_API = (  # noqa: WPS115
        "EDIT_FEATURE_API",
        _("CH__EDIT_FEATURE_API"),
    )
    EDIT_FEATURE_ISSUES = (  # noqa: WPS115
        "EDIT_FEATURE_ISSUES",
        _("CH__EDIT_FEATURE_ISSUES"),
    )
    EDIT_TERMS = "EDIT_TERMS", _("CH__EDIT_TERMS")  # noqa: WPS115
    EDIT_MODEL = "EDIT_MODEL", _("CH__EDIT_MODEL")  # noqa: WPS115
    EDIT_MODULES = "EDIT_MODULES", _("CH__EDIT_MODULES")  # noqa: WPS115
    EDIT_SPRINTS = "EDIT_SPRINTS", _("CH__EDIT_SPRINTS")  # noqa: WPS115
    VIEW_CONTRACT = "VIEW_CONTRACT", _("CH__VIEW_CONTRACT")  # noqa: WPS115
