from dataclasses import dataclass

from jnt_django_toolbox.models.fields import BitField

from apps.core.logic import queries
from apps.projects.models import Project, ProjectMember
from apps.users.models import User


@dataclass(frozen=True)
class MeProject:
    """Me project object."""

    role: str
    permissions: BitField


@dataclass(frozen=True)
class MeProjectQuery(queries.IQuery):
    """Me project query."""

    user: User
    project: Project


class QueryHandler(
    queries.IQueryHandler[
        MeProjectQuery,
        MeProject,
    ],
):
    """Found user by query."""

    def ask(self, query: MeProjectQuery) -> MeProject:
        """Handler."""
        role = query.project.public_role
        permissions = query.project.public_permissions

        if query.user.is_authenticated:
            member = ProjectMember.objects.filter(
                user=query.user,
                project=query.project,
            ).first()
            if member:
                role = member.role
                permissions = member.permissions

        return MeProject(
            role=role,
            permissions=permissions,
        )
