from jnt_admin_tools.mixins import AutocompleteFieldsAdminMixin

from apps.core.admin.inlines import BaseTabularInline
from apps.projects.models.project_member import ProjectMember


class ProjectMemberInline(AutocompleteFieldsAdminMixin, BaseTabularInline):
    """Project member inline."""

    model = ProjectMember
