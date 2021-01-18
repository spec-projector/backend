import django_filters


class UsersFilterSet(django_filters.FilterSet):
    """User filterset."""

    order_by = django_filters.OrderingFilter(fields=("email",))
    email = django_filters.CharFilter()
