from apps.core.admin.inlines import BaseTabularInline
from apps.projects.models.project_member import ProjectMember


class ProjectMemberInline(BaseTabularInline):
    """Project member inline."""

    model = ProjectMember
