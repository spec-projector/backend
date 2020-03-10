# -*- coding: utf-8 -*-

from typing import Optional

import graphene
from graphql import ResolveInfo

from apps.core.graphql.mutations import NoInputMutation


class LogoutMutation(NoInputMutation):
    """Logout mutation."""

    status = graphene.String()

    @classmethod
    def perform_mutate(
        cls, root: Optional[object], info: ResolveInfo,  # noqa: WPS110
    ) -> "LogoutMutation":
        """Perform mutation."""
        info.context.auth.delete()  # type: ignore

        return cls(status="success")
