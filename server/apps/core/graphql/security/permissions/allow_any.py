from typing import Optional

from graphql import ResolveInfo


class AllowAny:
    """
    Default authentication class.

    Allows any user for any action.
    Subclass it and override methods below.
    """

    def has_node_permission(
        self,
        info: ResolveInfo,  # noqa: WPS110
        obj_id: str,
    ) -> bool:
        """Check if have node permissions."""
        return True

    def has_mutation_permission(
        self,
        root: Optional[object],
        info: ResolveInfo,  # noqa: WPS110
        **kwargs,
    ) -> bool:
        """Check if have mutation permissions."""
        return True

    def has_filter_permission(
        self,
        info: ResolveInfo,  # noqa: WPS110
    ) -> bool:
        """Check if have filter permissions."""
        return True
