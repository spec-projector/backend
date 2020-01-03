# -*- coding: utf-8 -*-

from typing import Optional

import graphene
from graphql import ResolveInfo

from apps.core.graphql.mutations import NoInputMutation


class LogoutMutation(NoInputMutation):
    status = graphene.String()

    @classmethod
    def perform_mutate(
        cls,
        root: Optional[object],
        info: ResolveInfo,  # noqa: WPS110
    ) -> "LogoutMutation":
        info.context.auth.delete()

        return cls(status="success")
