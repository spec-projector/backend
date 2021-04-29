from apps.billing.logic.queries.change_subscription_request import (
    active as active_change_subscription_request,
)
from apps.billing.logic.queries.subscription import (
    active as active_subscription_request,
)
from apps.billing.logic.queries.tariff import list as list_tariffs
from apps.core.logic.queries import IQueryBus


def register_queries(queries_bus: IQueryBus):
    """Register queries handlers."""
    queries_bus.register_handler(
        active_change_subscription_request.GetActiveSubscriptionRequestQuery,
        active_change_subscription_request.QueryHandler,
    )

    queries_bus.register_handler(
        active_subscription_request.GetActiveSubscriptionQuery,
        active_subscription_request.QueryHandler,
    )

    queries_bus.register_handler(
        list_tariffs.ListTariffsQuery,
        list_tariffs.QueryHandler,
    )
