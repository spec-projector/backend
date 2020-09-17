# -*- coding: utf-8 -*-

from django.db.models import QuerySet
from graphql import ResolveInfo
from jnt_django_graphene_toolbox.connections import DataSourceConnection
from jnt_django_graphene_toolbox.relay_nodes import DatasourceRelayNode
from jnt_django_graphene_toolbox.types import BaseDjangoObjectType

from apps.users.models import User


class UserType(BaseDjangoObjectType):
    """User graphql type."""

    class Meta:
        model = User
        exclude = ("password",)
        interfaces = (DatasourceRelayNode,)
        connection_class = DataSourceConnection
        name = "User"

    @classmethod
    def get_queryset(
        cls,
        queryset: QuerySet,
        info: ResolveInfo,  # noqa: WPS110
    ) -> QuerySet:
        """Provides queryset."""
        if issubclass(queryset.model, User):
            queryset = queryset.filter(is_active=True)

        return queryset
