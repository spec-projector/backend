# -*- coding: utf-8 -*-

from typing import Optional

from graphql import ResolveInfo


class AllowAuthenticated:
    """Allows performing action only for logged in users."""

    def has_node_permission(self, info: ResolveInfo, obj_id: str) -> bool:
        if not info.context:
            return False

        return info.context.user.is_authenticated

    def has_mutation_permission(
        self,
        root: Optional[object],
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
