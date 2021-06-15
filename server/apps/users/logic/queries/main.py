from apps.users.logic.queries.user import access_tokens, allowed, find

QUERIES = (
    (allowed.Query, allowed.QueryHandler),
    (find.Query, find.QueryHandler),
    (access_tokens.Query, access_tokens.QueryHandler),
)
