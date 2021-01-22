from django.db import models

from apps.projects.models import ProjectMember
from apps.users.models import User


def get_available_projects(
    queryset: models.QuerySet,
    user: User,
) -> models.QuerySet:
    """Get available projects."""
    if user.is_anonymous:
        return queryset.filter(is_public=True)

    # all public projects, owner and project_member.
    # TODO: override (must be 1 queryset)
    return queryset.filter(
        id__in={
            *_get_public_project_ids(queryset),
            *_get_project_member_ids(user),
            *_get_project_owner_ids(user, queryset),
        },
    )


def get_projects_for_user(
    queryset: models.QuerySet,
    user: User,
) -> models.QuerySet:
    """Get projects for current user."""
    return queryset.filter(
        id__in={
            *_get_project_member_ids(user),
            *_get_project_owner_ids(user, queryset),
        },
    )


def _get_project_member_ids(user: User) -> models.QuerySet:
    """Get project ids for projectmember."""
    return ProjectMember.objects.filter(
        user_id=user.pk,
        roles__gt=0,
    ).values_list("project_id", flat=True)


def _get_project_owner_ids(
    user: User,
    queryset: models.QuerySet,
) -> models.QuerySet:
    """Get project ids for owner."""
    return queryset.filter(
        owner_id=user.pk,
    ).values_list("id", flat=True)


def _get_public_project_ids(queryset: models.QuerySet) -> models.QuerySet:
    """Get public project ids."""
    return queryset.filter(
        is_public=True,
    ).values_list("id", flat=True)
