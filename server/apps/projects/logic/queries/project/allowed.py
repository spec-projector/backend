from dataclasses import dataclass
from typing import Optional

from django.db import models

from apps.core.logic.queries import BaseQuery
from apps.projects.models import Project, ProjectMember
from apps.users.models import User


@dataclass(frozen=True)
class InputDto:
    """Get users query input data."""

    user: User
    queryset: Optional[models.QuerySet] = None
    include_public: bool = False


class Query(BaseQuery):
    """Allowed for user query."""

    def execute(self, input_dto: InputDto) -> models.QuerySet:
        """Handler."""
        projects = input_dto.queryset
        if projects is None:
            projects = Project.objects.all()

        if input_dto.user.is_anonymous:
            return projects.filter(is_public=True)

        project_ids = [
            *self._get_project_member_ids(input_dto.user),
            *self._get_project_owner_ids(input_dto.user, projects),
        ]

        if input_dto.include_public:
            project_ids.extend(self._get_public_project_ids(projects))

        return projects.filter(id__in=set(project_ids))

    def _get_public_project_ids(
        self,
        queryset: models.QuerySet,
    ) -> models.QuerySet:
        return queryset.filter(
            is_public=True,
        ).values_list("id", flat=True)

    def _get_project_member_ids(self, user: User) -> models.QuerySet:
        return ProjectMember.objects.filter(
            user_id=user.pk,
            roles__gt=0,
        ).values_list("project_id", flat=True)

    def _get_project_owner_ids(
        self,
        user: User,
        queryset: models.QuerySet,
    ) -> models.QuerySet:
        return queryset.filter(
            owner_id=user.pk,
        ).values_list("id", flat=True)
