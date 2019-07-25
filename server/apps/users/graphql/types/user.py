from apps.core.graphql.connections import DataSourceConnection
from apps.core.graphql.relay_nodes import DatasourceRelayNode
from apps.core.graphql.types import BaseDjangoObjectType
from apps.users.models import User


class UserType(BaseDjangoObjectType):
    class Meta:
        model = User
        exclude_fields = ('password',)
        interfaces = (DatasourceRelayNode,)
        connection_class = DataSourceConnection
        name = 'User'
