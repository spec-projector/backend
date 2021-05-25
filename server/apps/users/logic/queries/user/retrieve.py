from dataclasses import dataclass
from typing import Optional

from apps.core.logic import queries
from apps.users.models import User


@dataclass(frozen=True)
class FindUserQuery(queries.IQuery):
    """Find user query."""

    email: str


class QueryHandler(
    queries.IQueryHandler[
        FindUserQuery,
        Optional[User],
    ],
):
    """Found user by query."""

    def ask(self, query: FindUserQuery) -> Optional[User]:
        """Handler."""
        return User.objects.filter(is_active=True, email=query.email).first()
