from rest_framework import serializers

from apps.projects.graphql.mutations.projects.inputs import ProjectMember
from apps.projects.models import Project


class UpdateProjectInput(serializers.ModelSerializer):
    """Update project input."""

    class Meta:
        model = Project
        fields = ("id", "title", "description", "users", "isPublic")

    id = serializers.PrimaryKeyRelatedField(  # noqa: WPS125, A003
        queryset=Project.objects,
    )
    title = serializers.CharField(required=False)
    description = serializers.CharField(required=False)
    isPublic = serializers.BooleanField(  # noqa: WPS115 N815
        required=False,
        source="is_public",
    )

    users = ProjectMember(
        many=True,
        required=False,
        write_only=True,
        source="members",
    )
