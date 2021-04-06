import graphene
from graphql import ResolveInfo
from jnt_django_graphene_toolbox.nodes import ModelRelayNode

from apps.users.graphql.fields import UserConnectionField
from apps.users.graphql.types import MeUserType, UserType


class UsersQueries(graphene.ObjectType):
    """Graphql users queries."""

    user = ModelRelayNode.Field(UserType)
    me = graphene.Field(MeUserType)
    all_users = UserConnectionField()

    def resolve_me(self, info: ResolveInfo):  # noqa: WPS110
        """Resolves current context user."""
        return info.context.user  # type: ignore
