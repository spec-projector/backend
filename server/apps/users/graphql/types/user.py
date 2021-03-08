import graphene
from django.db.models import QuerySet
from graphql import ResolveInfo
from jnt_django_graphene_toolbox.types import BaseModelObjectType

from apps.users.logic.queries.users import allowed
from apps.users.models import User


class UserType(BaseModelObjectType):
    """User graphql type."""

    class Meta:
        model = User

    login = graphene.String()
    name = graphene.String()
    email = graphene.String()
    is_staff = graphene.Boolean()
    is_active = graphene.Boolean()
    avatar = graphene.String()
    last_login = graphene.DateTime()

    @classmethod
    def get_queryset(
        cls,
        queryset: QuerySet,
        info: ResolveInfo,  # noqa: WPS110
    ) -> QuerySet:
        """Provides queryset."""
        return allowed.Query().execute(
            allowed.InputDto(
                user=info.context.user,  # type: ignore
            ),
        )
