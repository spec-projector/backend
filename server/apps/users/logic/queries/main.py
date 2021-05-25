from apps.users.logic.queries.user import allowed, retrieve

QUERIES = (
    (allowed.ListAllowedUsersQuery, allowed.QueryHandler),
    (retrieve.FindUserQuery, retrieve.QueryHandler),
)
