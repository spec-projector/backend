import injector

from apps.billing import services
from apps.billing.logic import interfaces


class BillingInfrastructureServicesModule(injector.Module):
    """Setup di for billing infrastructure services."""

    def configure(self, binder: injector.Binder) -> None:
        """Bind services."""
        binder.bind(interfaces.IPaymentService, services.PaymentService)
