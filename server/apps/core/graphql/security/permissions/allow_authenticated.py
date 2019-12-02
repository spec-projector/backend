# -*- coding: utf-8 -*-

from typing import Any

from graphql import ResolveInfo


class AllowAuthenticated:
    """Allows performing action only for logged in users."""

    def has_node_permission(self, info: ResolveInfo, id: str) -> bool:
        if not info.context:
            return False

        return info.context.user.is_authenticated

    def has_mutation_permission(
        self,
        root: Any,
        info: ResolveInfo,
        **kwargs,
    ) -> bool:
        if not info.context:
            return False

        return info.context.user.is_authenticated

    def has_filter_permission(self, info: ResolveInfo) -> bool:
        if not info.context:
            return False

        return info.context.user.is_authenticated
