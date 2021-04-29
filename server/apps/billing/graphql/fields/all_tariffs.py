from django.db import models
from graphql import ResolveInfo

from apps.billing.graphql.types import TariffType
from apps.billing.logic.queries.tariff import list
from apps.core.graphql.fields.new_query_connection import (
    BaseNewQueryConnectionField,
)
from apps.core.logic import queries


class TariffConnectionField(BaseNewQueryConnectionField):
    """Handler for tariff collection."""

    query = list.ListTariffsQuery

    def __init__(self):
        """Initialize."""
        super().__init__(TariffType)

    @classmethod
    def build_query(
        cls,
        queryset: models.QuerySet,
        info: ResolveInfo,  # noqa: WPS110
        args,
    ) -> queries.IQuery:
        """Prepare query input data."""
        return cls.query(
            queryset=queryset,
            filters=list.TariffFilter(
                is_active=True,
            ),
            sort=args.get("sort"),
        )
