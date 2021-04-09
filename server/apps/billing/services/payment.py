import json
import logging

from cloudpayments import TransactionStatus
from django.utils.translation import gettext_lazy as _

from apps.billing.logic.interfaces import IPaymentService
from apps.billing.logic.interfaces.payment import PaymentInfo
from apps.core.services.errors import BaseInfrastructureError

PAYED_STATUSES = frozenset(
    (
        TransactionStatus.AUTHORIZED,
        TransactionStatus.COMPLETED,
    ),
)
OPERATION_TYPE_PAYMENT = "Payment"


class BasePaymentServiceError(BaseInfrastructureError):
    """Base payment error."""


class NotPaymentWebhookError(BasePaymentServiceError):
    """Webhook is not for payment."""

    code = "webhook_not_payment"
    message = _("MSG_WEBHOOK_NOT_PAYMENT")


class PaymentService(IPaymentService):
    """Cloud payment service."""

    def handle_payment_webhook(
        self,
        payment_data: dict[str, str],
        payment_meta: dict[str, str],
    ) -> PaymentInfo:
        """Handle payment webhook."""
        operation_type = payment_data["OperationType"]
        if payment_data["OperationType"] != OPERATION_TYPE_PAYMENT:
            logging.debug(
                "CloudPayment webhook with type '{0}': skip".format(
                    operation_type,
                ),
            )

            raise NotPaymentWebhookError()

        custom_data = json.loads(payment_data["Data"])

        return PaymentInfo(
            user_id=int(custom_data["user"]),
            request_hash=custom_data["hash"],
            user_email=payment_data["Email"],
            merchant_id=payment_data["SubscriptionId"],
            is_payed=payment_data["Status"] in PAYED_STATUSES,
        )
