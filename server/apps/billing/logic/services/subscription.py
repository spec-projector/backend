import logging
from datetime import datetime
from typing import Optional

from dateutil import relativedelta
from django.db import transaction
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from apps.billing.models import ChangeSubscriptionRequest, Subscription, Tariff
from apps.billing.models.enums import SubscriptionStatus
from apps.core.logic.errors import BaseApplicationError
from apps.users.models import User

logger = logging.getLogger(__name__)


class BaseSubscriptionError(BaseApplicationError):
    """Base subscription error."""


class SameTariffChangeError(BaseSubscriptionError):
    """Invalid tariff error."""

    code = "same_tariff_change"
    message = _("MSG__SAME_TARIFF_CHANGE")


class SubscriptionService:
    """Service for subscription management."""

    def get_user_subscription(self, user: User) -> Optional[Subscription]:
        """Retrieve active user subscription."""
        subscription = user.subscriptions.order_by("-created_at").first()
        if subscription and subscription.status == SubscriptionStatus.ACTIVE:
            return subscription

        return None

    def get_user_change_subscription_request(
        self,
        user: User,
    ) -> Optional[ChangeSubscriptionRequest]:
        """Retrieve active user change subscription request."""
        requests = user.change_subscriptions_requests
        return requests.filter(is_active=True).order_by("-created_at").first()

    def create_change_subscription_request(
        self,
        user: User,
        tariff: Tariff,
        request_hash: str,
    ) -> ChangeSubscriptionRequest:
        """Generate change subscription request."""
        request = ChangeSubscriptionRequest.objects.filter(
            user=user,
            hash=request_hash,
        ).first()
        if request:
            return request

        current_subscription = self.get_user_subscription(user)
        is_same_tariff = (
            current_subscription and current_subscription.tariff == tariff
        )
        if is_same_tariff:
            raise SameTariffChangeError()

        with transaction.atomic():
            ChangeSubscriptionRequest.objects.filter(user=user).update(
                is_active=False,
            )

            request = ChangeSubscriptionRequest(
                user=user,
                tariff=tariff,
                hash=request_hash,
            )
            request.full_clean()
            request.save()

        logger.info(
            "Change subscription request '{0}' was created".format(request),
        )

        return request

    def change_user_subscription(
        self,
        request: ChangeSubscriptionRequest,
        merchant_id: str,
    ) -> Subscription:
        """Change user subscription."""
        current_subscription = self.get_user_subscription(request.user)
        is_same_tariff = (
            current_subscription
            and current_subscription.tariff == request.tariff
        )
        if is_same_tariff:
            raise SameTariffChangeError()

        with transaction.atomic():
            new_subscription = self._change_subscription(
                request,
                current_subscription,
                merchant_id,
            )

        logger.info(
            "Subscription for user '{0}' was changed from '{1}'[id:{2}] to '{3}'[id: {4}]".format(  # noqa: E501
                request.user,
                request.from_subscription or "none",
                request.from_subscription.pk
                if request.from_subscription
                else "-",
                request.to_subscription,
                request.to_subscription.pk,
            ),
        )

        return new_subscription

    def _change_subscription(
        self,
        request: ChangeSubscriptionRequest,
        current_subscription: Subscription,
        merchant_id: str,
    ) -> Subscription:
        new_subscription = Subscription(
            user=request.user,
            status=SubscriptionStatus.ACTIVE,
            tariff=request.tariff,
            merchant_id=merchant_id,
            active_until=self._get_active_until(),
        )
        new_subscription.full_clean()
        new_subscription.save()

        if current_subscription:
            current_subscription.status = SubscriptionStatus.CANCELED
            current_subscription.full_clean()
            current_subscription.save()

        request.from_subscription = current_subscription
        request.to_subscription = new_subscription
        request.save()

        return new_subscription

    def _get_active_until(self) -> datetime:
        return timezone.now() + relativedelta.relativedelta(months=1)
