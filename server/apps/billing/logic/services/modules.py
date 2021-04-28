import injector

from apps.billing.logic import interfaces, services


class BillingLogicServicesModule(injector.Module):
    """Setup di for billing services."""

    def configure(self, binder: injector.Binder) -> None:
        """Bind services."""
        binder.bind(
            interfaces.ISubscriptionService,
            services.SubscriptionService,
        )
        binder.bind(
            interfaces.IUserTariffService,
            services.UserTariffService,
        )
