from dataclasses import dataclass
from typing import Optional

import injector

from apps.billing.logic.interfaces import ISubscriptionService
from apps.billing.models import Subscription
from apps.core.logic import queries
from apps.users.models import User


@dataclass(frozen=True)
class Query(queries.IQuery):
    """User active subscription."""

    user: User


class QueryHandler(queries.IQueryHandler[Query, Optional[Subscription]]):
    """User active subsription query."""

    @injector.inject
    def __init__(self, subscription_service: ISubscriptionService):
        """Initialize."""
        self._subscription_service = subscription_service

    def ask(self, query: Query) -> Optional[Subscription]:
        """Handler."""
        return self._subscription_service.get_user_subscription(query.user)
