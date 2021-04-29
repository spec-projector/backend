from dataclasses import dataclass
from typing import Optional

import injector

from apps.billing.logic.interfaces import ISubscriptionService
from apps.billing.models import ChangeSubscriptionRequest
from apps.core.logic import queries
from apps.users.models import User


@dataclass(frozen=True)
class GetActiveSubscriptionRequestQuery(queries.IQuery):
    """User active change subscription request."""

    user: User


class QueryHandler(
    queries.IQueryHandler[
        GetActiveSubscriptionRequestQuery,
        Optional[ChangeSubscriptionRequest],
    ],
):
    """User active subsription query."""

    @injector.inject
    def __init__(self, subscription_service: ISubscriptionService):
        """Initialize."""
        self._subscription_service = subscription_service

    def ask(
        self,
        query: GetActiveSubscriptionRequestQuery,
    ) -> Optional[ChangeSubscriptionRequest]:
        """Handler."""
        return self._subscription_service.get_user_change_subscription_request(
            query.user,
        )
