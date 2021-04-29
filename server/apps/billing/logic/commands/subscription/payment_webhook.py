import logging
from dataclasses import dataclass
from typing import Dict

import injector
from django.utils.translation import gettext_lazy as _

from apps.billing.logic.interfaces import IPaymentService, ISubscriptionService
from apps.billing.logic.interfaces.payment import PaymentInfo
from apps.billing.models import ChangeSubscriptionRequest, Tariff
from apps.core.logic import commands
from apps.core.logic.errors import BaseApplicationError
from apps.users.models import User

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class HandlePaymentWebhookCommand(commands.ICommand):
    """Process payment webhook."""

    payment_data: Dict[str, str]
    payment_meta: Dict[str, str]
    raw_body: bytes


class BasePaymentWebhookError(BaseApplicationError):
    """Base error for webhook."""


class UserNotFoundPaymentWebhookError(BasePaymentWebhookError):
    """User not found error."""

    code = "payment_user_not_found"
    message = _("MSG_USER_NOT_FOUND")


class UserInactivePaymentWebhookError(BasePaymentWebhookError):
    """User inactive error."""

    code = "payment_user_inactive"
    message = _("MSG_USER_INACTIVE")


class ChangeRequestInactivePaymentWebhookError(BasePaymentWebhookError):
    """Change subscription request inactive error."""

    code = "payment_change_request_inactive"
    message = _("MSG_CHANGE_SUBSCRIPTION_REQUEST_INACTIVE")


class CommandHandler(
    commands.ICommandHandler[HandlePaymentWebhookCommand, None],
):
    """Accept payment notification."""

    @injector.inject
    def __init__(
        self,
        subscription_service: ISubscriptionService,
        payment_service: IPaymentService,
    ):
        """Initialize."""
        self._subscription_service = subscription_service
        self._payment_service = payment_service

    def execute(self, command: HandlePaymentWebhookCommand) -> None:
        """Main logic here."""
        payment_info = self._payment_service.handle_payment_webhook(
            command.payment_data,
            command.payment_meta,
            command.raw_body,
        )
        user = self._get_user(payment_info)
        request = self._get_change_request(user, payment_info)
        self._subscription_service.change_user_subscription(
            request,
            payment_info.merchant_id,
        )

    def _get_user(self, payment_info: PaymentInfo) -> User:
        logger.debug(
            "Getting user [id: {0}, email: {1}] for change subscription".format(
                payment_info.user_id,
                payment_info.user_email,
            ),
        )
        try:
            user = User.objects.get(
                id=payment_info.user_id,
                email=payment_info.user_email,
            )
        except User.DoesNotExist:
            raise UserNotFoundPaymentWebhookError()

        if not user.is_active:
            logger.debug("User '{0}' is inactive".format(user))
            raise UserInactivePaymentWebhookError()
        return user

    def _get_change_request(
        self,
        user: User,
        payment_info: PaymentInfo,
    ) -> ChangeSubscriptionRequest:
        logger.debug(
            "Getting change subscription request [user: {0}, hash: {1}]".format(
                user,
                payment_info.request_hash,
            ),
        )

        try:
            request = ChangeSubscriptionRequest.objects.get(
                user=user,
                hash=payment_info.request_hash,
            )
        except ChangeSubscriptionRequest.DoesNotExist:
            request = (
                self._subscription_service.create_change_subscription_request(
                    user,
                    Tariff.objects.get(id=payment_info.tariff_id),
                    payment_info.request_hash,
                )
            )

        if not request.is_active:
            logger.debug(
                "Change subscription request '{0}' is inactive".format(
                    request,
                ),
            )
            raise ChangeRequestInactivePaymentWebhookError()
        return request
