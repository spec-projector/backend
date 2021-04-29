from apps.core.logic.queries import IQueryBus
from apps.projects.logic.queries.issue import retrieve
from apps.projects.logic.queries.project import allowed
from apps.projects.logic.queries.project_member import active


def register_queries(queries_bus: IQueryBus):
    """Register queries handlers."""
    queries_bus.register_handler(
        allowed.ListAllowedProjectsQuery,
        allowed.QueryHandler,
    )
    queries_bus.register_handler(retrieve.GetIssueQuery, retrieve.QueryHandler)
    queries_bus.register_handler(
        active.ListActiveProjectMembersQuery,
        active.QueryHandler,
    )
