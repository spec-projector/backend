# -*- coding: utf-8 -*-

from typing import Optional

import graphene
from graphql import ResolveInfo

from apps.core.graphql.errors import GraphQLPermissionDenied
from apps.core.graphql.security.mixins.mutation import AuthMutation
from apps.core.graphql.security.permissions import AllowAuthenticated


class NoInputMutation(AuthMutation, graphene.Mutation):
    """Base class for mutations without parameters."""

    permission_classes = (AllowAuthenticated,)

    class Meta:
        abstract = True

    @classmethod
    def mutate(
        cls,
        root: Optional[object],
        info: ResolveInfo,  # noqa: WPS110
    ):
        """Perform mutation."""
        cls.check_premissions(root, info)

        return cls.perform_mutate(root, info)

    @classmethod
    def check_premissions(
        cls,
        root: Optional[object],
        info: ResolveInfo,  # noqa: WPS110
    ) -> None:
        """Check if have permissions."""
        if not cls.has_permission(root, info):
            raise GraphQLPermissionDenied()

    @classmethod
    def perform_mutate(
        cls,
        root: Optional[object],
        info: ResolveInfo,  # noqa: WPS110
    ) -> "NoInputMutation":
        """Perform mutation."""
        raise NotImplementedError
