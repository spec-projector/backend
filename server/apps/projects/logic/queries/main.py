from apps.projects.logic.queries.issue import retrieve
from apps.projects.logic.queries.project import allowed
from apps.projects.logic.queries.project_member import active

QUERIES = (
    (allowed.ListAllowedProjectsQuery, allowed.QueryHandler),
    (retrieve.GetIssueQuery, retrieve.QueryHandler),
    (active.ListActiveProjectMembersQuery, active.QueryHandler),
)
