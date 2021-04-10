import base64
import hashlib
import hmac
import json
import logging
from typing import Dict

from cloudpayments import TransactionStatus
from constance import config
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


class WrongSignatureError(BasePaymentServiceError):
    """Request wrong signature."""

    code = "webhook_wrong_signature"
    message = _("MSG_WEBHOOK_WRONG_SIGNATURE")


class PaymentService(IPaymentService):
    """Cloud payment service."""

    def handle_payment_webhook(
        self,
        payment_data: Dict[str, str],
        payment_meta: Dict[str, str],
        raw_body: bytes,
    ) -> PaymentInfo:
        """Handle payment webhook."""
        self._validate_request(raw_body, payment_meta)

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
            tariff_id=int(custom_data["tariff"]),
            request_hash=custom_data["hash"],
            user_email=payment_data["Email"],
            merchant_id=payment_data["SubscriptionId"],
            is_payed=payment_data["Status"] in PAYED_STATUSES,
        )

    def _validate_request(self, raw: bytes, payment_meta: Dict[str, str]):
        # based on https://developers.cloudpayments.ru/#proverka-uvedomleniy
        if not config.CLOUD_PAYMENT_API_SECRET:
            return

        signature = base64.b64encode(
            hmac.new(
                bytes(config.CLOUD_PAYMENT_API_SECRET, "utf-8"),
                raw,
                digestmod=hashlib.sha256,
            ).digest(),
        )

        req_signature = payment_meta.get("Content-Hmac")
        is_valid = req_signature and req_signature == signature.decode("utf-8")
        if not is_valid:
            raise WrongSignatureError()
