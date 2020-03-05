# -*- coding: utf-8 -*-

from typing import Optional

from graphql import ResolveInfo


class AllowStaff:
    """Allow performing action only for staff users."""

    def has_node_permission(
        self,
        info: ResolveInfo,  # noqa: WPS110
        obj_id: str,
    ) -> bool:
        return info.context.user.is_staff  # type: ignore

    def has_mutation_permission(
        self,
        root: Optional[object],
        info: ResolveInfo,  # noqa: WPS110
        **kwargs,
    ) -> bool:
        return info.context.user.is_staff  # type: ignore

    def has_filter_permission(
        self,
        info: ResolveInfo,  # noqa: WPS110
    ) -> bool:
        return info.context.user.is_staff  # type: ignore
