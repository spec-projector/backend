import graphene
from jnt_django_graphene_toolbox.connection_fields import (
    DataSourceConnectionField,
)

from apps.projects.graphql.filters import ProjectsFilterSet
from apps.projects.graphql.relay_nodes import ProjectDatasourceRelayNode
from apps.projects.graphql.types import ProjectType


class ProjectsQueries(graphene.ObjectType):
    """Project graphql queries."""

    project = ProjectDatasourceRelayNode.Field(ProjectType)
    all_projects = DataSourceConnectionField(
        ProjectType,
        filterset_class=ProjectsFilterSet,
    )
