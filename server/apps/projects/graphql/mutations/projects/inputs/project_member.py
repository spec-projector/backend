# -*- coding: utf-8 -*-

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.core.serializers.fields import BitField
from apps.projects.models.project_member import PROJECT_MEMBER_ROLES
from apps.users.models import User


class ProjectMember(serializers.Serializer):
    id = serializers.PrimaryKeyRelatedField(  # noqa: A003
        queryset=User.objects,
        source="user",
    )
    roles = BitField(
        choices=PROJECT_MEMBER_ROLES,
    )

    def validate_roles(self, roles):
        if not roles:
            raise ValidationError("Roles not setted")
        return roles
