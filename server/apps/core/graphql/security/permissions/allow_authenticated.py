from typing import Any

from graphql import ResolveInfo


class AllowAuthenticated:
    """
    Allows performing action only for logged in users.
    """

    @staticmethod
    def has_node_permission(info: ResolveInfo, id: str) -> bool:
        if not info.context:
            return False

        return info.context.user.is_authenticated

    @staticmethod
    def has_mutation_permission(
        root: Any,
        info: ResolveInfo,
        **kwargs,
    ) -> bool:
        if not info.context:
            return False

        return info.context.user.is_authenticated

    @staticmethod
    def has_filter_permission(info: ResolveInfo) -> bool:
        if not info.context:
            return False

        return info.context.user.is_authenticated
