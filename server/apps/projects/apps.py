from django.utils.translation import gettext_lazy as _

from apps.core.utils.apps import BaseAppConfig


class AppConfig(BaseAppConfig):
    """App configuration."""

    name = "apps.projects"
    verbose_name = _("VN__PROJECTS")
