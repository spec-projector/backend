from apps.core.logic.queries import IQueryBus
from apps.projects.logic.queries.issue import retrieve
from apps.projects.logic.queries.project import allowed


def register_queries(queries_bus: IQueryBus):
    """Register queries handlers."""
    queries_bus.register_handler(
        allowed.ListAllowedProjectsQuery,
        allowed.QueryHandler,
    )
    queries_bus.register_handler(retrieve.GetIssueQuery, retrieve.QueryHandler)
