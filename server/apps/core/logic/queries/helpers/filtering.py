import dataclasses
import typing as ty

import django_filters
from django.db import models

from apps.core.logic.errors import InvalidInputApplicationError
from apps.core.utils.objects import empty


def filter_queryset(
    queryset: models.QuerySet,
    filterset_class: ty.Type[django_filters.FilterSet],
    filters,
) -> models.QuerySet:
    """Filter queryset."""
    if not filters:
        return queryset

    filters = {
        data_key: data_value
        for data_key, data_value in dataclasses.asdict(filters).items()
        if data_value != empty
    }

    if not filters:
        return queryset

    filterset = filterset_class(data=filters, queryset=queryset)
    if not filterset.is_valid():
        raise InvalidInputApplicationError(filterset.errors)

    return filterset.qs
