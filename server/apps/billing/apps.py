from django.utils.translation import gettext_lazy as _

from apps.core import injector
from apps.core.utils.apps import BaseAppConfig


class AppConfig(BaseAppConfig):
    """App configuration."""

    name = "apps.billing"
    verbose_name = _("VN__BILLING")

    def ready(self):
        """Trigger on app ready."""
        self._setup_dependency_injection()
        super().ready()

    def _setup_dependency_injection(self):
        from apps.billing.services.modules import (  # noqa: WPS433
            BillingInfrastructureServicesModule,
        )
        from apps.billing.logic.services.modules import (  # noqa: WPS433
            BillingLogicServicesModule,
        )

        injector.binder.install(BillingLogicServicesModule)
        injector.binder.install(BillingInfrastructureServicesModule)
