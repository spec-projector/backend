import django_filters
from django.db import models

from apps.projects.services.projects.available_projects import (
    get_projects_for_user,
)


class ProjectsFilterSet(django_filters.FilterSet):
    """Projects filterset."""

    order_by = django_filters.OrderingFilter(fields=("created_at",))
    title = django_filters.CharFilter()

    def filter_queryset(self, queryset) -> models.QuerySet:
        """Filter by is_public."""
        projects = super().filter_queryset(queryset)

        return get_projects_for_user(projects, self.request.user)
