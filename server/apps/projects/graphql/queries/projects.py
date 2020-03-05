# -*- coding: utf-8 -*-

import graphene

from apps.core.graphql.connection_fields import DataSourceConnectionField
from apps.core.graphql.relay_nodes import DatasourceRelayNode
from apps.projects.graphql.filters import ProjectsFilterSet
from apps.projects.graphql.types import ProjectType


class ProjectsQueries(graphene.ObjectType):
    """Project graphql queries."""

    project = DatasourceRelayNode.Field(ProjectType)
    all_projects = DataSourceConnectionField(
        ProjectType,
        filterset_class=ProjectsFilterSet,
    )
