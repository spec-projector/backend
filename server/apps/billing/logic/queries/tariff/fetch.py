from dataclasses import dataclass
from enum import Enum
from typing import Optional, Union

import django_filters
from django.db.models import QuerySet

from apps.billing.models import Tariff
from apps.core.logic.queries import BaseQuery, SortHandler
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
class InputDto:
    """Get tariffs query input data."""

    filters: Optional[TariffFilter] = None
    sort: TariffSort = TariffSort.ORDER_DESC
    queryset: Optional[QuerySet] = None


class Query(BaseQuery):
    """Tariffs query."""

    filterset_class = _TariffsFilterSet
    sort_handler = SortHandler(TariffSort)

    def execute(self, input_dto: InputDto) -> QuerySet:
        """Handler."""
        queryset = (
            Tariff.objects.all()
            if input_dto.queryset is None
            else input_dto.queryset
        )
        queryset = self.filter_queryset(queryset, input_dto.filters)
        return self.sort_queryset(queryset, input_dto.sort)
