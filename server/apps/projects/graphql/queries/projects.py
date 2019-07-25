import graphene

from apps.core.graphql.connection_fields import DataSourceConnectionField
from apps.core.graphql.relay_nodes import DatasourceRelayNode
from apps.projects.graphql.types import ProjectType
from apps.projects.graphql.filters import ProjectsFilterSet


class ProjectsQueries(graphene.ObjectType):
    project = DatasourceRelayNode.Field(ProjectType)
    all_projects = DataSourceConnectionField(
        ProjectType,
        filterset_class=ProjectsFilterSet
    )
