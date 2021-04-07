from dataclasses import dataclass
from typing import Optional

from apps.billing.logic.services import SubscriptionService
from apps.billing.models import ChangeSubscriptionRequest
from apps.core import injector
from apps.users.models import User


@dataclass(frozen=True)
class InputDto:
    """User active change subscription request."""

    user: User


class Query:
    """User active subsription query."""

    def execute(
        self,
        input_dto: InputDto,
    ) -> Optional[ChangeSubscriptionRequest]:
        """Handler."""
        service = injector.get(SubscriptionService)
        return service.get_user_change_subscription_request(input_dto.user)
