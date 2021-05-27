from dataclasses import dataclass
from typing import Optional

from jnt_django_toolbox.models.fields import BitField

from apps.core.logic import queries
from apps.projects.models import Project, ProjectMember
from apps.users.models import User


@dataclass(frozen=True)
class ProjectMe:
    """Me project object."""

    role: str
    permissions: BitField


@dataclass(frozen=True)
class ProjectMeQuery(queries.IQuery):
    """Me project query."""

    user: Optional[User]
    project: Project


class QueryHandler(
    queries.IQueryHandler[
        ProjectMeQuery,
        ProjectMe,
    ],
):
    """Found user by query."""

    def ask(self, query: ProjectMeQuery) -> ProjectMe:
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
