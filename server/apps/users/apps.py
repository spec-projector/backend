from django.utils.translation import gettext_lazy as _

from apps.core import injector
from apps.core.utils.apps import BaseAppConfig


class AppConfig(BaseAppConfig):
    """Class represents the "users" application."""

    name = "apps.users"
    verbose_name = _("VN__USERS")

    def ready(self):
        """Trigger on app ready."""
        super().ready()

        self._setup_dependency_injection()

    def _setup_dependency_injection(self) -> None:
        from apps.users.services.modules import (  # noqa: WPS433
            UserInfrastructureServicesModule,
        )
        from apps.users.logic.services.modules import (  # noqa: WPS433
            UserLogicServicesModule,
        )
        from apps.users.logic.commands.modules import (  # noqa: WPS433
            UserCommandsModule,
        )

        injector.binder.install(UserInfrastructureServicesModule)
        injector.binder.install(UserLogicServicesModule)
        injector.binder.install(UserCommandsModule)
