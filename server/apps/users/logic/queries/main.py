from apps.users.logic.queries.user import allowed, find

QUERIES = (
    (allowed.Query, allowed.QueryHandler),
    (find.Query, find.QueryHandler),
)
