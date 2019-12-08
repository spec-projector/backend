# -*- coding: utf-8 -*-

from django.db.models import QuerySet
from graphql import ResolveInfo

from apps.core.graphql.connections import DataSourceConnection
from apps.core.graphql.relay_nodes import DatasourceRelayNode
from apps.core.graphql.types import BaseDjangoObjectType
from apps.projects.models import Project


class ProjectType(BaseDjangoObjectType):
    class Meta:
        model = Project
        interfaces = (DatasourceRelayNode,)
        connection_class = DataSourceConnection
        name = 'Project'

    @classmethod
    def get_queryset(
        cls,
        queryset: QuerySet,
        info: ResolveInfo,  # noqa: WPS110
    ) -> QuerySet:
        """Get queryset."""
        return queryset.filter(owner=info.context.user)
