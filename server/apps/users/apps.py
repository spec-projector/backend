from django.utils.translation import gettext_lazy as _

from apps.core import injector
from apps.core.logic.commands import ICommandBus
from apps.core.logic.queries import IQueryBus
from apps.core.utils.apps import BaseAppConfig


class AppConfig(BaseAppConfig):
    """Class represents the "users" application."""

    name = "apps.users"
    verbose_name = _("VN__USERS")

    def ready(self):
        """Trigger on app ready."""
        from apps.users.logic.commands import COMMANDS  # noqa: WPS433
        from apps.users.logic.queries import QUERIES  # noqa: WPS433

        super().ready()

        self._setup_dependency_injection()

        injector.get(ICommandBus).register_many(COMMANDS)
        injector.get(IQueryBus).register_many(QUERIES)

    def _setup_dependency_injection(self) -> None:
        from apps.users.services.modules import (  # noqa: WPS433
            UserInfrastructureServicesModule,
        )
        from apps.users.logic.services.modules import (  # noqa: WPS433
            UserLogicServicesModule,
        )

        injector.binder.install(UserInfrastructureServicesModule)
        injector.binder.install(UserLogicServicesModule)
