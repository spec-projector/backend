# -*- coding: utf-8 -*-

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.core.serializers.fields import BitField
from apps.projects.models.project_member import ProjectMemberRole
from apps.users.models import User


class ProjectMember(serializers.Serializer):
    """Project member serializer."""

    id = serializers.PrimaryKeyRelatedField(  # noqa: A003
        queryset=User.objects,
        source="user",
    )
    roles = BitField(choices=ProjectMemberRole.choices)

    def validate_roles(self, roles):
        """Roles validation."""
        if not roles:
            raise ValidationError("Roles not setted")
        return roles
