# -*- coding: utf-8 -*-

from typing import Any

from graphql import ResolveInfo


class AllowStaff:
    """Allow performing action only for staff users."""

    def has_node_permission(self, info: ResolveInfo, obj_id: str) -> bool:
        return info.context.user.is_staff

    def has_mutation_permission(
        self,
        root: Any,
        info: ResolveInfo,
        **kwargs,
    ) -> bool:
        return info.context.user.is_staff

    def has_filter_permission(self, info: ResolveInfo) -> bool:
        return info.context.user.is_staff
