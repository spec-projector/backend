import graphene
from graphql import ResolveInfo
from jnt_django_graphene_toolbox.errors import GraphQLPermissionDenied

from apps.core.logic import queries
from apps.users.graphql.types import MeUserType, UserType
from apps.users.logic.queries.user import find
from apps.users.models import User


class UsersQueries(graphene.ObjectType):
    """Graphql users queries."""

    me = graphene.Field(MeUserType)
    find_user = graphene.Field(UserType, email=graphene.String(required=True))

    def resolve_me(self, info: ResolveInfo):  # noqa: WPS110
        """Resolves current context user."""
        if not info.context.user.is_authenticated:  # type: ignore
            return None

        return info.context.user  # type: ignore

    def resolve_find_user(
        self,
        info: ResolveInfo,  # noqa: WPS110
        **kwargs,
    ) -> User:
        """Resolve user."""
        user = info.context.user  # type: ignore
        if not user.is_authenticated:
            raise GraphQLPermissionDenied()

        return queries.execute_query(find.Query(kwargs["email"]))
