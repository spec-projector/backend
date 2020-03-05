# -*- coding: utf-8 -*-

from rest_framework import serializers

from apps.projects.graphql.mutations.projects.inputs import ProjectMember
from apps.projects.models import Project


class UpdateProjectInput(serializers.ModelSerializer):
    """Update project input."""

    id = serializers.PrimaryKeyRelatedField(  # noqa: A003
        queryset=Project.objects,
    )
    title = serializers.CharField(required=False)
    description = serializers.CharField(required=False)
    public = serializers.BooleanField(required=False)

    users = ProjectMember(
        many=True,
        required=False,
        write_only=True,
        source="members",
    )

    class Meta:
        model = Project
        fields = ("id", "title", "description", "users", "public")
