import abc
from typing import Optional

from apps.billing.models import ChangeSubscriptionRequest, Subscription, Tariff
from apps.users.models import User


class ISubscriptionService(abc.ABC):
    """Subscription service interface."""

    @abc.abstractmethod
    def get_user_subscription(self, user: User) -> Optional[Subscription]:
        """Retrieve active user subscription."""

    @abc.abstractmethod
    def get_user_change_subscription_request(
        self,
        user: User,
    ) -> Optional[ChangeSubscriptionRequest]:
        """Retrieve active user change subscription request."""

    @abc.abstractmethod
    def create_change_subscription_request(
        self,
        user: User,
        tariff: Tariff,
        request_hash: str,
    ) -> ChangeSubscriptionRequest:
        """Generate change subscription request."""

    @abc.abstractmethod
    def change_user_subscription(
        self,
        request: ChangeSubscriptionRequest,
        merchant_id: str,
    ) -> Subscription:
        """Change user subscription."""

    @abc.abstractmethod
    def add_default_subscription(self, user: User) -> Optional[Subscription]:
        """Add default subscription to a user."""
