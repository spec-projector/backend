from typing import Optional

from apps.billing.models import Subscription
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
