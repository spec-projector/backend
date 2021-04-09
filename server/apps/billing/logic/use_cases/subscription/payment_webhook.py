import logging
from dataclasses import dataclass

import injector
from django.utils.translation import gettext_lazy as _

from apps.billing.logic.interfaces import IPaymentService
from apps.billing.logic.interfaces.payment import PaymentInfo
from apps.billing.logic.services import SubscriptionService
from apps.billing.models import ChangeSubscriptionRequest
from apps.core.logic.errors import BaseApplicationError
from apps.core.logic.use_cases import BaseUseCase
from apps.users.models import User

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class InputDto:
    """Delete project input dto."""

    payment_data: dict[str, str]
    payment_meta: dict[str, str]


class BasePaymentWebhookError(BaseApplicationError):
    """Base error for webhook."""


class UserNotFoundPaymentWebhookError(BasePaymentWebhookError):
    """User not found error."""

    code = "payment_user_not_found"
    message = _("MSG_PAYMENT_USER_NOT_FOUND")


class UserInactivePaymentWebhookError(BasePaymentWebhookError):
    """User inactive error."""

    code = "payment_user_inactive"
    message = _("MSG_PAYMENT_USER_INACTIVE")


class ChangeRequestNotFoundPaymentWebhookError(BasePaymentWebhookError):
    """Change subscription request not found error."""

    code = "payment_change_request_not_found"
    message = _("MSG_PAYMENT_CHANGE_REQUEST_NOT_FOUND")


class ChangeRequestInactivePaymentWebhookError(BasePaymentWebhookError):
    """Change subscription request inactive error."""

    code = "payment_change_request_inactive"
    message = _("MSG_PAYMENT_CHANGE_REQUEST_INACTIVE")


class UseCase(BaseUseCase):
    """Use case for accepting payment notification."""

    @injector.inject
    def __init__(
        self,
        subscription_service: SubscriptionService,
        payment_service: IPaymentService,
    ):
        """Initialize."""
        self._subscription_service = subscription_service
        self._payment_service = payment_service

    def execute(self, input_dto: InputDto):
        """Main logic here."""
        payment_info = self._payment_service.handle_payment_webhook(
            input_dto.payment_data,
            input_dto.payment_meta,
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
                is_active=True,
            )
        except ChangeSubscriptionRequest.DoesNotExist:
            raise ChangeRequestNotFoundPaymentWebhookError()

        if not request.is_active:
            logger.debug(
                "Change subscription request '{0}' is inactive".format(
                    request,
                ),
            )
            raise ChangeRequestInactivePaymentWebhookError()
        return request
