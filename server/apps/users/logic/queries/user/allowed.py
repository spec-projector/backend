from dataclasses import dataclass

from django.db import models

from apps.core.logic.queries.handler import BaseQueryHandler
from apps.users.models import User


@dataclass(frozen=True)
class ListAllowedUsersQuery:
    """Allowed users query."""

    user: User


class QueryHandler(BaseQueryHandler[ListAllowedUsersQuery, models.QuerySet]):
    """Users query."""

    def ask(self, query: ListAllowedUsersQuery) -> models.QuerySet:
        """Handler."""
        return User.objects.filter(is_active=True)
