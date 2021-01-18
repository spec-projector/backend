import graphene
from jnt_django_graphene_toolbox.nodes import ModelRelayNode

from apps.users.graphql.fields import UserConnectionField
from apps.users.graphql.resolvers import resolve_me_user
from apps.users.graphql.types import UserType


class UsersQueries(graphene.ObjectType):
    """Graphql users queries."""

    user = ModelRelayNode.Field(UserType)
    me = graphene.Field(UserType, resolver=resolve_me_user)
    all_users = UserConnectionField()
