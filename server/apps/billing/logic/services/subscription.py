from typing import Optional

from django.db import transaction
from django.utils.translation import gettext_lazy as _

from apps.billing.models import ChangeSubscriptionRequest, Subscription, Tariff
from apps.billing.models.enums import SubscriptionStatus
from apps.core.logic.errors import BaseApplicationError
from apps.users.models import User


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

        return request

    def change_user_subscription(self, request: ChangeSubscriptionRequest):
        """Change user subscription."""
        current_subscription = self.get_user_subscription(request.user)
        is_same_tariff = (
            current_subscription
            and current_subscription.tariff == request.tariff
        )
        if is_same_tariff:
            raise SameTariffChangeError()

        with transaction.atomic():
            new_subscription = Subscription(
                user=request.user,
                status=SubscriptionStatus.ACTIVE,
                tariff=request.tariff,
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
