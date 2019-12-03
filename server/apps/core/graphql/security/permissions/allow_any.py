# -*- coding: utf-8 -*-

from typing import Any

from graphql import ResolveInfo


class AllowAny:
    """
    Default authentication class.

    Allows any user for any action.
    Subclass it and override methods below.
    """

    def has_node_permission(self, info: ResolveInfo, obj_id: str) -> bool:
        return True

    def has_mutation_permission(
        self,
        root: Any,
        info: ResolveInfo,
        **kwargs,
    ) -> bool:
        return True

    def has_filter_permission(self, info: ResolveInfo) -> bool:
        return True
