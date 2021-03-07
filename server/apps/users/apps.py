from django.utils.translation import gettext_lazy as _

from apps.core import injector
from apps.core.utils.apps import BaseAppConfig


class AppConfig(BaseAppConfig):
    """Class represents the "users" application."""

    name = "apps.users"
    verbose_name = _("VN__USERS")

    def ready(self):
        """Trigger on app ready."""
        from apps.users.services.modules import (  # noqa: WPS433
            UserInfrastructureServicesModule,
        )
        from apps.users.logic.services.modules import (  # noqa: WPS433
            UserLogicServicesModule,
        )

        super().ready()

        injector.binder.install(UserInfrastructureServicesModule)
        injector.binder.install(UserLogicServicesModule)
