from dataclasses import dataclass
from enum import Enum
from typing import Union

import django_filters
from django.db.models import QuerySet

from apps.core.logic.queries import BaseQuery
from apps.core.logic.queries.sort import SortHandler
from apps.core.utils.objects import Empty, empty
from apps.users.models import User


class UserSort(Enum):
    """Allowed sort fields."""

    EMAIL_ASC = "email"  # noqa: WPS115
    EMAIL_DESC = "-email"  # noqa: WPS115


@dataclass(frozen=True)
class UserFilter:
    """Users collection filters."""

    email: Union[Empty, str] = empty


class _UsersFilterSet(django_filters.FilterSet):
    """User filterset."""

    email = django_filters.CharFilter()


@dataclass(frozen=True)
class InputDto:
    """Get users query input data."""

    user: User
    filters: UserFilter
    sort: UserSort
    queryset: QuerySet


class Query(BaseQuery):
    """Users query."""

    filterset_class = _UsersFilterSet
    sort_handler = SortHandler(UserSort)

    def execute(self, input_dto: InputDto) -> QuerySet:
        """Handler."""
        queryset = (
            input_dto.queryset
            if input_dto.queryset is not None
            else User.objects.all()
        )
        queryset = self.filter_queryset(queryset, input_dto.filters)
        return self.sort_queryset(queryset, input_dto.sort)
