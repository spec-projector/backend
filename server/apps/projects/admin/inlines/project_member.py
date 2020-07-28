# -*- coding: utf-8 -*-

from jnt_admin_tools.mixins import AdminAutocompleteFieldsMixin

from apps.core.admin.inlines import BaseTabularInline
from apps.projects.models.project_member import ProjectMember


class ProjectMemberInline(AdminAutocompleteFieldsMixin, BaseTabularInline):
    """Project member inline."""

    model = ProjectMember
