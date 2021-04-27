from apps.core.logic.queries import IQueryBus
from apps.users.logic.queries.user import allowed


def register_queries(queries_bus: IQueryBus):
    """Register queries handlers."""
    queries_bus.register_handler(
        allowed.ListAllowedUsersQuery,
        allowed.QueryHandler,
    )
