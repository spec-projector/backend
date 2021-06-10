from apps.projects.logic.queries.issue import retrieve
from apps.projects.logic.queries.project import allowed, project_me
from apps.projects.logic.queries.project_member import active

QUERIES = (
    (allowed.Query, allowed.QueryHandler),
    (retrieve.Query, retrieve.QueryHandler),
    (active.Query, active.QueryHandler),
    (project_me.Query, project_me.QueryHandler),
)
