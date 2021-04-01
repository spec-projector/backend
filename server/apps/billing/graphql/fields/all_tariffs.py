from django.db.models import QuerySet
from graphql import ResolveInfo

from apps.billing.graphql.types import TariffType
from apps.billing.logic.queries.tariff import fetch
from apps.core.graphql.fields import BaseQueryConnectionField


class TariffConnectionField(BaseQueryConnectionField):
    """Handler for tariff collection."""

    query = fetch.Query

    def __init__(self):
        """Initialize."""
        super().__init__(TariffType)

    @classmethod
    def get_input_dto(
        cls,
        queryset: QuerySet,
        info: ResolveInfo,  # noqa: WPS110
        args,
    ):
        """Prepare query input data."""
        return fetch.InputDto(
            queryset=queryset,
            filters=cls.get_filters_from_args(args, fetch.TariffFilter),
            sort=cls.get_sort_from_args(args),
        )
