from apps.billing.logic.queries.change_subscription_request import active
from apps.core.logic.queries import IQueryBus


def register_queries(queries_bus: IQueryBus):
    """Register queries handlers."""
    queries_bus.register_handler(
        active.GetActiveSubscriptionQuery,
        active.QueryHandler,
    )
