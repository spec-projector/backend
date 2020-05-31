# -*- coding: utf-8 -*-

from graphene import Connection, Int
from graphql import ResolveInfo


class DataSourceConnection(Connection):
    """Datasource connection."""

    class Meta:
        abstract = True

    count = Int()

    def resolve_count(self, info: ResolveInfo):  # noqa: WPS110
        """Provides collection lenght."""
        return self.length
