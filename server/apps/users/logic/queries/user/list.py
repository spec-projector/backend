from dataclasses import dataclass
from enum import Enum
from typing import Optional, Union

import django_filters
from django.db import models

from apps.core.logic.queries.handler import BaseQueryHandler
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
    is_active: Union[Empty, bool] = empty


class _UsersFilterSet(django_filters.FilterSet):
    """User filterset."""

    email = django_filters.CharFilter()
    is_active = django_filters.BooleanFilter()


@dataclass(frozen=True)
class ListUsersQuery:
    """List users query."""

    user: User
    filters: Optional[UserFilter] = None
    sort: Optional[UserSort] = None
    queryset: Optional[models.QuerySet] = None


class QueryHandler(BaseQueryHandler[ListUsersQuery, models.QuerySet]):
    """Users query."""

    filterset_class = _UsersFilterSet
    sort_handler = SortHandler(UserSort)

    def ask(self, query: ListUsersQuery) -> models.QuerySet:
        """Handler."""
        queryset = (
            User.objects.all() if query.queryset is None else query.queryset
        )
        queryset = self.filter_queryset(queryset, query.filters)
        return self.sort_queryset(queryset, query.sort)
