import graphene
from django.db.models import QuerySet
from graphql import ResolveInfo

from apps.core.graphql.fields import BaseQueryConnectionField
from apps.users.graphql.types import UserType
from apps.users.logic.queries import users


class UserConnectionField(BaseQueryConnectionField):
    """Handler for user collection."""

    query = users.Query

    def __init__(self):
        """Initialize."""
        super().__init__(
            UserType,
            email=graphene.String(),
        )

    @classmethod
    def get_input_dto(
        cls,
        queryset: QuerySet,
        info: ResolveInfo,  # noqa: WPS110
        args,
    ):
        """Prepare query input data."""
        return users.InputDto(
            user=info.context.user,  # type: ignore
            sort=cls.get_sort_from_args(args),
            filters=cls.get_filters_from_args(args),
            queryset=queryset,
        )
