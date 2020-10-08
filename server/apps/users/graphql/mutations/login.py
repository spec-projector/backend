from typing import Dict, Optional

import graphene
from graphql import ResolveInfo
from jnt_django_graphene_toolbox.mutations import SerializerMutation

from apps.core.graphql.security.permissions import AllowAny
from apps.users.graphql.mutations.inputs.login import LoginMutationInput
from apps.users.graphql.types import TokenType
from apps.users.services.auth import login_user


class LoginMutation(SerializerMutation):
    """Login mutation."""

    class Meta:
        serializer_class = LoginMutationInput

    permission_classes = (AllowAny,)

    token = graphene.Field(TokenType)

    @classmethod
    def perform_mutate(
        cls,
        root: Optional[object],
        info: ResolveInfo,  # noqa: WPS110
        validated_data: Dict[str, str],
    ) -> "LoginMutation":
        """Perform mutation."""
        token = login_user(
            validated_data["username"],
            validated_data["password"],
        )

        return cls(token=token)
