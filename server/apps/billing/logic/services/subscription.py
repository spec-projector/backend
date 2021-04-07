from typing import Optional

from django.db import transaction

from apps.billing.models import ChangeSubscriptionRequest, Subscription, Tariff
from apps.billing.models.enums import SubscriptionStatus
from apps.users.models import User


class SubscriptionService:
    """Service for subscription management."""

    def get_user_subscription(self, user: User) -> Optional[Subscription]:
        """Retrieve active user subscription."""
        subscription = user.subscriptions.latest("created_at")
        if subscription.status == SubscriptionStatus.ACTIVE:
            return subscription

        return None

    def get_user_change_subscription_request(
        self,
        user: User,
    ) -> Optional[ChangeSubscriptionRequest]:
        """Retrieve active user change subscription request."""
        return user.change_subscriptions_requests.filter(
            is_active=True,
        ).latest("created_at")

    def change_user_subscription(
        self,
        user: User,
        tariff: Tariff,
        request_hash: str,
    ) -> ChangeSubscriptionRequest:
        """Generate change subscription request."""
        subscription = self.get_user_subscription(user)

        with transaction.atomic():
            ChangeSubscriptionRequest.objects.filter(user=user).update(
                is_active=False,
            )

            request = ChangeSubscriptionRequest(
                user=user,
                tariff=tariff,
                from_subscription=subscription,
                hash=request_hash,
            )
            request.full_clean()
            request.save()

        return request
