# -*- coding: utf-8 -*-

from graphql import ResolveInfo

from apps.core.graphql.security.permissions import AllowAuthenticated
from apps.projects.models import Project


class AllowAuthenticatedOrPublicProject(AllowAuthenticated):
    """Allows get public project or logged in users."""

    def has_node_permission(
        self,
        info: ResolveInfo,  # noqa: WPS110
        obj_id: str,
    ) -> bool:
        has_node_permission = super().has_node_permission(info, obj_id)

        if has_node_permission:
            return has_node_permission

        return Project.objects.filter(id=obj_id, public=True).exists()
