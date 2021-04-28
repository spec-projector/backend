import abc
import dataclasses
from typing import Dict, Generic, Type, TypeVar

import django_filters
from django.db import models

from apps.core.logic.errors import InvalidInputApplicationError
from apps.core.logic.queries import SortHandler
from apps.core.utils.objects import empty

TInput = TypeVar("TInput")


class BaseQuery(Generic[TInput], metaclass=abc.ABCMeta):
    """Represents base query."""

    filterset_class: Type[django_filters.FilterSet]
    sort_handler: SortHandler = None

    @abc.abstractmethod
    def execute(self, input_dto: TInput) -> models.QuerySet:
        """Main logic here."""

    def sort_queryset(
        self,
        queryset: models.QuerySet,
        sort,
    ) -> models.QuerySet:
        """Sort queryset."""
        if not self.sort_handler:
            return queryset

        return self.sort_handler.filter(queryset, sort)

    def filter_queryset(
        self,
        queryset: models.QuerySet,
        filters,
    ) -> models.QuerySet:
        """Filter queryset."""
        if not filters or not self.filterset_class:
            return queryset

        filters = self._prepare_filters(filters)

        if not filters:
            return queryset

        filterset = self.filterset_class(
            data=filters,
            queryset=queryset,
        )
        if not filterset.is_valid():
            raise InvalidInputApplicationError(filterset.errors)

        return filterset.qs

    def _prepare_filters(self, filters) -> Dict[str, object]:
        return {
            data_key: data_value
            for data_key, data_value in dataclasses.asdict(filters).items()
            if data_value != empty
        }
