from django.utils.translation import gettext_lazy as _

from apps.core import injector
from apps.core.utils.apps import BaseAppConfig


class AppConfig(BaseAppConfig):
    """App configuration."""

    name = "apps.projects"
    verbose_name = _("VN__PROJECTS")

    def ready(self):
        """Trigger on app ready."""
        from apps.projects.services.modules import (  # noqa: WPS433
            ProjectServicesModule,
        )

        super().ready()

        injector.binder.install(ProjectServicesModule)
