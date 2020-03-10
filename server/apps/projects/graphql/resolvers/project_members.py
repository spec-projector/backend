# -*- coding: utf-8 -*-

from django.db.models import QuerySet
from graphql import ResolveInfo

from apps.projects.models import Project, ProjectMember


def resolve_project_members(
    project: Project, info: ResolveInfo, **kwargs,  # noqa: WPS110
) -> QuerySet:
    """Resolves project members."""
    return ProjectMember.objects.filter(project=project, user__is_active=True)
