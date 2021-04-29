from apps.billing.logic.queries.change_subscription_request import (
    active as active_change_subscription_request,
)
from apps.billing.logic.queries.subscription import (
    active as active_subscription_request,
)
from apps.billing.logic.queries.tariff import list as list_tariffs

QUERIES = (
    (
        active_change_subscription_request.GetActiveSubscriptionRequestQuery,
        active_change_subscription_request.QueryHandler,
    ),
    (
        active_subscription_request.GetActiveSubscriptionQuery,
        active_subscription_request.QueryHandler,
    ),
    (list_tariffs.ListTariffsQuery, list_tariffs.QueryHandler),
)
