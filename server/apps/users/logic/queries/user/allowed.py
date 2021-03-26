from dataclasses import dataclass

from django.db.models import QuerySet

from apps.core.logic.queries import BaseQuery
from apps.users.models import User


@dataclass(frozen=True)
class InputDto:
    """Get users query input data."""

    user: User


class Query(BaseQuery):
    """Users query."""

    def execute(self, input_dto: InputDto) -> QuerySet:
        """Handler."""
        return User.objects.filter(is_active=True)
