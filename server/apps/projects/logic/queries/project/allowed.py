from dataclasses import dataclass
from enum import Enum
from typing import Optional

import django_filters
from django.db import models

from apps.core.logic import queries
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
class ListAllowedProjectsQuery(queries.IQuery):
    """List allowed projects."""

    user: User
    queryset: Optional[models.QuerySet] = None
    sort: Optional[ProjectSort] = None
    filters: Optional[ProjectFilter] = None
    include_public: bool = False


class QueryHandler(
    queries.IQueryHandler[ListAllowedProjectsQuery, models.QuerySet],
):
    """Allowed projects for user query."""

    def ask(self, query: ListAllowedProjectsQuery) -> models.QuerySet:
        """Handler."""
        projects = query.queryset
        if projects is None:
            projects = Project.objects.all()

        if query.user.is_anonymous:
            return projects.filter(is_public=True)

        project_ids = [
            *self._get_project_member_ids(query.user),
            *self._get_project_owner_ids(query.user, projects),
        ]

        if query.include_public:
            project_ids.extend(self._get_public_project_ids(projects))

        projects = projects.filter(id__in=set(project_ids))
        return queries.sort_queryset(
            queries.filter_queryset(
                projects,
                _ProjectFilterSet,
                query.filters,
            ),
            queries.SortHandler(ProjectSort),
            query.sort,
        )

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
        ).values_list("project_id", flat=True)

    def _get_project_owner_ids(
        self,
        user: User,
        queryset: models.QuerySet,
    ) -> models.QuerySet:
        return queryset.filter(
            owner_id=user.pk,
        ).values_list("id", flat=True)
