from dataclasses import dataclass

from django.db import models

from apps.core.logic import queries
from apps.users.models import User


@dataclass(frozen=True)
class ListAllowedUsersQuery:
    """Allowed users query."""

    user: User


class QueryHandler(
    queries.IQueryHandler[ListAllowedUsersQuery, models.QuerySet],
):
    """Users query."""

    def ask(self, query: ListAllowedUsersQuery) -> models.QuerySet:
        """Handler."""
        return User.objects.filter(is_active=True)
