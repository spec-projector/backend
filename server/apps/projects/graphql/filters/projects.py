# -*- coding: utf-8 -*-

import django_filters

from apps.projects.models.project import Project


class ProjectsFilterSet(django_filters.FilterSet):
    """Projects filterset."""

    class Meta:
        model = Project
        fields = ("title",)

    order_by = django_filters.OrderingFilter(fields=("created_at",))
