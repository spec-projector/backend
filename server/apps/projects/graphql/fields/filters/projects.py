import django_filters
from django.db import models

from apps.projects.logic.queries.project import allowed


class ProjectsFilterSet(django_filters.FilterSet):
    """Projects filterset."""

    title = django_filters.CharFilter()

    def filter_queryset(self, queryset) -> models.QuerySet:
        """Filter for user."""
        queryset = super().filter_queryset(queryset)

        return allowed.Query().execute(
            allowed.InputDto(
                user=self.request.user,
                queryset=queryset,
            ),
        )
