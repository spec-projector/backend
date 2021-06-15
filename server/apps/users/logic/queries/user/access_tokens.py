from dataclasses import dataclass

from django.db import models

from apps.core.logic import queries
from apps.users.models import User


@dataclass(frozen=True)
class Query(queries.IQuery):
    """User access tokens."""

    user: User


class QueryHandler(queries.IQueryHandler[Query, models.QuerySet]):
    """User active access tokens."""

    def ask(self, query: Query) -> models.QuerySet:
        """Handler."""
        return query.user.access_tokens.all()
