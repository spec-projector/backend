from typing import Any

from graphql import ResolveInfo


class AllowSuperuser:
    """
    Allow performing action only for superusers.
    """

    def has_node_permission(self, info: ResolveInfo, id: str) -> bool:
        return info.context.user.is_superuser

    def has_mutation_permission(
        self,
        root: Any,
        info: ResolveInfo,
        **kwargs,
    ) -> bool:
        return info.context.user.is_superuser

    def has_filter_permission(self, info: ResolveInfo) -> bool:
        return info.context.user.is_superuser
