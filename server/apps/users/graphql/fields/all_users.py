import graphene
from jnt_django_graphene_toolbox.fields import BaseModelConnectionField

from apps.users.graphql.filters import UsersFilterSet
from apps.users.graphql.types import UserType


class UserConnectionField(BaseModelConnectionField):
    """Handler for user collection."""

    filterset_class = UsersFilterSet

    def __init__(self):
        """Initialize."""
        super().__init__(
            UserType,
            order_by=graphene.String(),
            email=graphene.String(),
        )
