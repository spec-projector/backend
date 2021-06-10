from dataclasses import dataclass
from typing import Optional

from jnt_django_toolbox.models.fields.bit.types import BitHandler

from apps.core.logic import queries
from apps.core.utils.bit_field import get_all_selected_bitfield
from apps.projects.models import Project, ProjectMember
from apps.projects.models.enums import ProjectMemberRole, ProjectPermission
from apps.users.models import User


@dataclass(frozen=True)
class ProjectMe:
    """Me project object."""

    role: str
    permissions: BitHandler


@dataclass(frozen=True)
class Query(queries.IQuery):
    """Me project query."""

    user: Optional[User]
    project: Project


class QueryHandler(queries.IQueryHandler[Query, ProjectMe]):
    """Found user by query."""

    def ask(self, query: Query) -> ProjectMe:
        """Handler."""
        me_project_permissions = self._get_member_permissions(
            query.user,
            query.project,
        )
        if not me_project_permissions:
            me_project_permissions = ProjectMe(
                role=query.project.public_role,
                permissions=query.project.public_permissions,
            )
        return me_project_permissions

    def _get_member_permissions(self, user, project) -> Optional[ProjectMe]:
        """Get project member permissions."""
        if not user:
            return None

        if project.owner == user:
            return ProjectMe(
                role=ProjectMemberRole.EDITOR,
                permissions=get_all_selected_bitfield(ProjectPermission),
            )

        member = ProjectMember.objects.filter(
            user=user,
            project=project,
        ).first()

        if not member:
            return None

        return ProjectMe(
            role=member.role,
            permissions=member.permissions,
        )
