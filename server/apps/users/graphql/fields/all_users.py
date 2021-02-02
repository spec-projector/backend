import graphene
from jnt_django_graphene_toolbox.fields import BaseModelConnectionField
from jnt_django_graphene_toolbox.filters import SortHandler

from apps.users.graphql.filters import UsersFilterSet
from apps.users.graphql.types import UserType


class UserSort(graphene.Enum):
    """Allowed sort fields."""

    EMAIL_ASC = "email"  # noqa: WPS115
    EMAIL_DESC = "-email"  # noqa: WPS115


class UserConnectionField(BaseModelConnectionField):
    """Handler for user collection."""

    filterset_class = UsersFilterSet
    sort_handler = SortHandler(UserSort)

    def __init__(self):
        """Initialize."""
        super().__init__(
            UserType,
            email=graphene.String(),
        )
