# -*- coding: utf-8 -*-

import django_filters

from apps.users.models import User


class UsersFilterSet(django_filters.FilterSet):
    """User filterset."""

    class Meta:
        model = User
        fields = ("email",)

    order_by = django_filters.OrderingFilter(fields=("email",))
