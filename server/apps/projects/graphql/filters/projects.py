import django_filters

from apps.projects.models.project import Project


class ProjectsFilterSet(django_filters.FilterSet):
    order_by = django_filters.OrderingFilter(
        fields=('created_at',)
    )

    class Meta:
        model = Project
        fields = ('title',)
