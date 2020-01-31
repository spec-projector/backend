# -*- coding: utf-8 -*-

from apps.core.graphql.connections import DataSourceConnection
from apps.core.graphql.relay_nodes import DatasourceRelayNode
from apps.core.graphql.types import BaseDjangoObjectType
from apps.projects.models import ProjectMember


class ProjectMemberType(BaseDjangoObjectType):
    class Meta:
        model = ProjectMember
        interfaces = (DatasourceRelayNode,)
        connection_class = DataSourceConnection
        name = "ProjectMember"
