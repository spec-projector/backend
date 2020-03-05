# -*- coding: utf-8 -*-

from typing import Dict, Optional

import graphene
from django.contrib.auth import REDIRECT_FIELD_NAME
from graphql import ResolveInfo
from social_core.actions import do_complete
from social_django.views import _do_login  # noqa: WPS436

from apps.core.graphql.mutations import SerializerMutation
from apps.core.graphql.security.permissions import AllowAny
from apps.users.graphql.mutations.helpers.psa import page_social_auth
from apps.users.graphql.mutations.inputs.gl_complete_auth import (
    GitLabCompleteAuthMutationInput,
)
from apps.users.graphql.types import TokenType
from apps.users.models import Token


class GitlabAuthError(Exception):
    """Gitlab authentication error."""


class GitLabCompleteAuthMutation(SerializerMutation):
    """Gitlab complete auth mutation."""

    permission_classes = (AllowAny,)

    token = graphene.Field(TokenType)

    class Meta:
        serializer_class = GitLabCompleteAuthMutationInput

    @classmethod
    def perform_mutate(
        cls,
        root: Optional[object],
        info: ResolveInfo,  # noqa: WPS110
        validated_data: Dict[str, str],
    ) -> "GitLabCompleteAuthMutation":
        """Perform mutation."""
        request = page_social_auth(info.context)
        request.backend.set_data(**validated_data)

        complete_result = do_complete(
            request.backend,
            _do_login,
            user=None,
            redirect_name=REDIRECT_FIELD_NAME,
            request=request,
        )

        if not isinstance(complete_result, Token):
            raise GitlabAuthError(complete_result.content.decode())

        return cls(token=complete_result)
