from jnt_django_graphene_toolbox.connections import DataSourceConnection
from jnt_django_graphene_toolbox.relay_nodes import DatasourceRelayNode
from jnt_django_graphene_toolbox.types import BaseDjangoObjectType

from apps.projects.models import ProjectMember


class ProjectMemberType(BaseDjangoObjectType):
    """Project member type."""

    class Meta:
        model = ProjectMember
        interfaces = (DatasourceRelayNode,)
        connection_class = DataSourceConnection
        name = "ProjectMember"
