import django_filters


class ProjectsFilterSet(django_filters.FilterSet):
    """Projects filterset."""

    order_by = django_filters.OrderingFilter(fields=("created_at",))
    title = django_filters.CharFilter()
