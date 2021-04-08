import graphene
from graphql import ResolveInfo

from apps.users.graphql.types import MeUserType


class UsersQueries(graphene.ObjectType):
    """Graphql users queries."""

    me = graphene.Field(MeUserType)

    def resolve_me(self, info: ResolveInfo):  # noqa: WPS110
        """Resolves current context user."""
        if not info.context.user.is_authenticated:  # type: ignore
            return None

        return info.context.user  # type: ignore
