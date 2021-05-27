from apps.projects.logic.queries.issue import retrieve
from apps.projects.logic.queries.project import allowed, me_project
from apps.projects.logic.queries.project_member import active

QUERIES = (
    (allowed.ListAllowedProjectsQuery, allowed.QueryHandler),
    (retrieve.GetIssueQuery, retrieve.QueryHandler),
    (active.ListActiveProjectMembersQuery, active.QueryHandler),
    (me_project.MeProjectQuery, me_project.QueryHandler),
)
