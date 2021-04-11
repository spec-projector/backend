from django.utils.translation import gettext_lazy as _

from apps.core import injector
from apps.core.utils.apps import BaseAppConfig


class AppConfig(BaseAppConfig):
    """App configuration."""

    name = "apps.projects"
    verbose_name = _("VN__PROJECTS")

    def ready(self):
        """Trigger on app ready."""
        super().ready()

        self._setup_dependency_injection()

    def _setup_dependency_injection(self):
        from apps.projects.services.modules import (  # noqa: WPS433
            ProjectInfrastructureServicesModule,
        )

        from apps.projects.logic.services.modules import (  # noqa: WPS433
            ProjectLogicServicesModule,
        )

        injector.binder.install(ProjectInfrastructureServicesModule)
        injector.binder.install(ProjectLogicServicesModule)
