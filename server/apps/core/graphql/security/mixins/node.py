from typing import Optional

from django.db.models import Model
from graphql import ResolveInfo
from jnt_django_graphene_toolbox.errors import GraphQLPermissionDenied

from apps.core.graphql.security.permissions import AllowAny


class AuthNode:
    """
    Permission mixin for queries (nodes).

    Allows for simple configuration of access to nodes via class system.
    """

    permission_classes = (AllowAny,)

    @classmethod
    def get_node(
        cls,
        info: ResolveInfo,  # noqa: WPS110
        id: str,  # noqa: WPS125, A003, A002
    ) -> Optional[Model]:
        """Provides node."""
        has_node_permission = all(
            (
                perm().has_node_permission(info, id)
                for perm in cls.permission_classes
            ),
        )

        if not has_node_permission:
            raise GraphQLPermissionDenied()

        queryset = cls.get_queryset(  # type: ignore
            cls._meta.model.objects,  # type: ignore
            info,
        )

        try:
            return queryset.get(id=id)
        except cls._meta.model.DoesNotExist:  # type: ignore
            return None
