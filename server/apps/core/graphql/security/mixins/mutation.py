# -*- coding: utf-8 -*-

from typing import Optional

from graphql import ResolveInfo

from apps.core.graphql.security.permissions import AllowAny


class AuthMutation:
    """Permission mixin for ClientIdMutation."""

    permission_classes = (AllowAny,)

    @classmethod
    def has_permission(
        cls,
        root: Optional[object],
        info: ResolveInfo,  # noqa: WPS110
        **kwargs,
    ) -> bool:
        """Check if have permissions."""
        return all(
            perm().has_mutation_permission(root, info, **kwargs)
            for perm in cls.permission_classes
        )
