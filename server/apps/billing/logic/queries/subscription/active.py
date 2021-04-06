from dataclasses import dataclass
from typing import Optional

from apps.billing.models import Subscription
from apps.billing.models.enums import SubscriptionStatus
from apps.users.models import User


@dataclass(frozen=True)
class InputDto:
    """User active subscription."""

    user: User


class Query:
    """User active subsription query."""

    def execute(self, input_dto: InputDto) -> Optional[Subscription]:
        """Handler."""
        subscription = input_dto.user.subscriptions.latest("created")
        if subscription.status == SubscriptionStatus.ACTIVE:
            return subscription
