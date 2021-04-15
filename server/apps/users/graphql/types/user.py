import graphene
from django.db.models import QuerySet
from graphql import ResolveInfo
from jnt_django_graphene_toolbox.types import BaseModelObjectType

from apps.core.utils.media import get_absolute_path
from apps.users.logic.queries.user import allowed
from apps.users.models import User


class UserType(BaseModelObjectType):
    """User graphql type."""

    class Meta:
        model = User

    first_name = graphene.String()
    last_name = graphene.String()
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

    def resolve_avatar(self, info):  # noqa: WPS110
        """Resolve image absolute path."""
        return get_absolute_path(self.avatar, info.context)
