import injector

from apps.billing.logic import services


class BillingLogicServicesModule(injector.Module):
    """Setup di for billing services."""

    def configure(self, binder: injector.Binder) -> None:
        """Bind services."""
        binder.bind(services.SubscriptionService)
