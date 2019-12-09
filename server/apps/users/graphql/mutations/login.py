# -*- coding: utf-8 -*-

from typing import Dict, Optional

import graphene
from graphql import ResolveInfo

from apps.core.graphql.mutations.serializer import SerializerMutation
from apps.core.graphql.security.permissions import AllowAny
from apps.users.graphql.mutations.inputs.login import LoginMutationInput
from apps.users.graphql.types import TokenType
from apps.users.services.auth import login_user


class LoginMutation(SerializerMutation):
    permission_classes = (AllowAny,)

    token = graphene.Field(TokenType)

    class Meta:
        serializer_class = LoginMutationInput

    @classmethod
    def perform_mutate(
        cls,
        root: Optional[object],
        info: ResolveInfo,  # noqa: WPS110
        validated_data: Dict[str, str],
    ) -> 'LoginMutation':
        token = login_user(
            validated_data['username'],
            validated_data['password'],
        )

        return cls(token=token)
