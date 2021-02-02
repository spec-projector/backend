import django_filters


class UsersFilterSet(django_filters.FilterSet):
    """User filterset."""

    email = django_filters.CharFilter()
