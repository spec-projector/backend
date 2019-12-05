# -*- coding: utf-8 -*-

import graphene

from apps.core.graphql.mutations import BaseMutation
from apps.core.graphql.security.permissions import AllowAny
from apps.users.graphql.mutations.inputs.login import LoginMutationInput
from apps.users.graphql.types import TokenType
from apps.users.services.auth import login_user


class LoginMutation(BaseMutation):
    permission_classes = (AllowAny,)
    token = graphene.Field(TokenType)

    class Meta:
        serializer_class = LoginMutationInput

    @classmethod
    def perform_mutate(
        cls,
        serializer: LoginMutationInput,
        info,
    ) -> 'LoginMutation':
        token = login_user(
            serializer.validated_data['username'],
            serializer.validated_data['password'],
        )

        return cls(token=token)
