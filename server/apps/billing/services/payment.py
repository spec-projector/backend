from cloudpayments import CloudPayments
from constance import config

from apps.billing.logic.interfaces import IPaymentService


class PaymentService(IPaymentService):
    """Cloud payment service."""

    def __init__(self):
        """Initialize."""
        self._client = CloudPayments(
            config.CLOUD_PAYMENT_PUBLIC_ID,
            config.CLOUD_PAYMENT_API_SECRET,
        )
        self._client.test()
