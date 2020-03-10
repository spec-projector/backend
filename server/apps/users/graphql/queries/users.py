# -*- coding: utf-8 -*-

import graphene

from apps.core.graphql.connection_fields import DataSourceConnectionField
from apps.core.graphql.relay_nodes import DatasourceRelayNode
from apps.users.graphql.filters import UsersFilterSet
from apps.users.graphql.resolvers import resolve_me_user
from apps.users.graphql.types import UserType


class UsersQueries(graphene.ObjectType):
    """Graphql users queries."""

    user = DatasourceRelayNode.Field(UserType)
    me = graphene.Field(UserType, resolver=resolve_me_user)
    all_users = DataSourceConnectionField(
        UserType, filterset_class=UsersFilterSet,
    )
