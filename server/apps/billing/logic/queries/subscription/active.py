from dataclasses import dataclass
from typing import Optional

from apps.billing.logic.interfaces import ISubscriptionService
from apps.billing.models import Subscription
from apps.core import injector
from apps.users.models import User


@dataclass(frozen=True)
class InputDto:
    """User active subscription."""

    user: User


class Query:
    """User active subsription query."""

    def execute(self, input_dto: InputDto) -> Optional[Subscription]:
        """Handler."""
        service = injector.get(ISubscriptionService)
        return service.get_user_subscription(input_dto.user)
