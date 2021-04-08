from dataclasses import dataclass
from enum import Enum
from typing import Optional

import django_filters
from django.db import models

from apps.core.logic.queries import BaseQuery
from apps.core.logic.queries.sort import SortHandler
from apps.projects.models import Project, ProjectMember
from apps.users.models import User


class ProjectSort(Enum):
    """Allowed sort fields."""

    CREATED_AT_ASC = "created_at"  # noqa: WPS115
    CREATED_AT_DESC = "-created_at"  # noqa: WPS115


class _ProjectFilterSet(django_filters.FilterSet):
    """Tariff filterSet."""

    title = django_filters.CharFilter()


@dataclass(frozen=True)
class ProjectFilter:
    """Project filter ."""

    title: str


@dataclass(frozen=True)
class InputDto:
    """Get users query input data."""

    user: User
    queryset: Optional[models.QuerySet] = None
    sort: Optional[ProjectSort] = None
    filters: Optional[ProjectFilter] = None
    include_public: bool = False


class Query(BaseQuery):
    """Allowed for user query."""

    filterset_class = _ProjectFilterSet
    sort_handler = SortHandler(ProjectSort)

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

        projects = projects.filter(id__in=set(project_ids))
        projects = self.filter_queryset(projects, input_dto.filters)
        return self.sort_queryset(projects, input_dto.sort)

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
