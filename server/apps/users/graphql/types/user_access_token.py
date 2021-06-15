import graphene
from jnt_django_graphene_toolbox.types import BaseModelObjectType

from apps.users.models import UserAccessToken


class UserAccessTokenType(BaseModelObjectType):
    """User access token graphql type."""

    class Meta:
        model = UserAccessToken

    name = graphene.String()
    created_at = graphene.DateTime()
