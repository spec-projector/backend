from jnt_django_graphene_toolbox.types import BaseDjangoObjectType

from apps.core.graphql.security.permissions import AllowAny
from apps.users.models import Token


class TokenType(BaseDjangoObjectType):
    """Token graphql type."""

    class Meta:
        model = Token
        name = "Token"

    permission_classes = (AllowAny,)
