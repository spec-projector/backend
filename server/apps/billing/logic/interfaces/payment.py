import abc
from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class PaymentInfo:
    """Payment info."""

    user_id: int
    tariff_id: int
    user_email: str
    merchant_id: str
    request_hash: str
    is_payed: bool


class IPaymentService(abc.ABC):
    """Payment service interface."""

    def handle_payment_webhook(
        self,
        payment_data: Dict[str, str],
        payment_meta: Dict[str, str],
    ) -> PaymentInfo:
        """Handle payment webhook."""
