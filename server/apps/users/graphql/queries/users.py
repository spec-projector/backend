# -*- coding: utf-8 -*-

import graphene

from apps.core.graphql.relay_nodes import DatasourceRelayNode
from apps.users.graphql.resolvers import resolve_me_user
from apps.users.graphql.types import UserType


class UsersQueries(graphene.ObjectType):
    user = DatasourceRelayNode.Field(UserType)
    me = graphene.Field(
        UserType,
        resolver=resolve_me_user
    )
