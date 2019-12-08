# -*- coding: utf-8 -*-

from typing import Optional

import graphene
from django.contrib.auth import REDIRECT_FIELD_NAME
from graphql import ResolveInfo
from social_core.actions import do_auth

from apps.core.graphql.mutations import NoInputMutation
from apps.core.graphql.security.permissions import AllowAny
from apps.users.graphql.mutations.helpers.psa import page_social_auth


class GitLabLoginMutation(NoInputMutation):
    permission_classes = (AllowAny,)

    redirect_url = graphene.String()

    @classmethod
    def perform_mutate(
        cls,
        root: Optional[object],
        info: ResolveInfo,  # noqa: WPS110
    ) -> 'GitLabLoginMutation':
        request = page_social_auth(info.context)

        response = do_auth(request.backend, redirect_name=REDIRECT_FIELD_NAME)

        return cls(redirect_url=response.url)
