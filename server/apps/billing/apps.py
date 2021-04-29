from django.utils.translation import gettext_lazy as _

from apps.core import injector
from apps.core.logic.commands import ICommandBus
from apps.core.logic.queries import IQueryBus
from apps.core.utils.apps import BaseAppConfig


class AppConfig(BaseAppConfig):
    """App configuration."""

    name = "apps.billing"
    verbose_name = _("VN__BILLING")

    def ready(self):
        """Trigger on app ready."""
        from apps.billing.logic.queries import register_queries  # noqa: WPS433
        from apps.billing.logic.commands import COMMANDS  # noqa: WPS433

        super().ready()
        self._setup_dependency_injection()
        injector.get(ICommandBus).register_many(COMMANDS)
        register_queries(injector.get(IQueryBus))

    def _setup_dependency_injection(self) -> None:
        from apps.billing.services.modules import (  # noqa: WPS433
            BillingInfrastructureServicesModule,
        )
        from apps.billing.logic.services.modules import (  # noqa: WPS433
            BillingLogicServicesModule,
        )

        injector.binder.install(BillingLogicServicesModule)
        injector.binder.install(BillingInfrastructureServicesModule)
