from dataclasses import dataclass
from enum import Enum
from typing import Optional, Union

import django_filters
from django.db import models

from apps.billing.models import Tariff
from apps.core.logic import queries
from apps.core.utils.objects import Empty, empty


class TariffSort(Enum):
    """Allowed sort fields."""

    ORDER_ASC = "order"  # noqa: WPS115
    ORDER_DESC = "-order"  # noqa: WPS115


@dataclass(frozen=True)
class TariffFilter:
    """Tariffs collection filters."""

    is_active: Union[Empty, bool] = empty


class _TariffsFilterSet(django_filters.FilterSet):
    """Tariff filterSet."""

    is_active = django_filters.BooleanFilter()


@dataclass(frozen=True)
class ListTariffsQuery(queries.IQuery):
    """Get tariffs query input data."""

    filters: Optional[TariffFilter] = None
    sort: TariffSort = TariffSort.ORDER_DESC
    queryset: Optional[models.QuerySet] = None


class QueryHandler(
    queries.IQueryHandler[ListTariffsQuery, models.QuerySet],
):
    """Tariffs query."""

    def ask(self, query: ListTariffsQuery) -> models.QuerySet:
        """Handler."""
        queryset = (
            Tariff.objects.all() if query.queryset is None else query.queryset
        )
        return queries.sort_queryset(
            queries.filter_queryset(
                queryset,
                _TariffsFilterSet,
                query.filters,
            ),
            queries.SortHandler(TariffSort),
            query.sort,
        )
