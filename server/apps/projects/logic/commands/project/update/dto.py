from dataclasses import dataclass
from typing import List, Union

from rest_framework import exceptions, serializers

from apps.core.serializers.fields import BitField
from apps.core.utils.objects import Empty, empty
from apps.media.models import Image
from apps.projects.logic.commands.project.dto import (
    FigmaIntegrationDto,
    FigmaIntegrationDtoValidator,
    GitHubIntegrationDto,
    GitHubIntegrationDtoValidator,
    GitLabIntegrationDto,
    GitLabIntegrationDtoValidator,
)
from apps.projects.models.enums import ProjectMemberRole, ProjectPermission
from apps.users.models import User


@dataclass(frozen=True)
class ProjectMemberDto:
    """Update project member data."""

    user: int
    roles: int


@dataclass(frozen=True)
class ProjectDto:
    """Create project data."""

    title: Union[str, Empty] = empty
    description: str = empty
    is_public: bool = empty
    figma_integration: Union[str, FigmaIntegrationDto] = empty
    github_integration: Union[str, GitHubIntegrationDto] = empty
    gitlab_integration: Union[str, GitLabIntegrationDto] = empty
    members: List[ProjectMemberDto] = empty
    emblem: int = empty
    public_role: str = empty
    public_permissions: int = empty


class _ProjectMemberValidator(serializers.Serializer):
    """Project member serializer."""

    id = serializers.PrimaryKeyRelatedField(  # noqa: WPS125
        queryset=User.objects,
        required=True,
    )
    permissions = BitField(choices=ProjectPermission.choices)
    role = serializers.ChoiceField(
        choices=ProjectMemberRole.choices,
        required=True,
    )

    def validate_permissions(self, permissions):
        """Roles validation."""
        if not permissions:
            raise exceptions.ValidationError("Permissions not set")
        return permissions


class ProjectDtoValidator(serializers.Serializer):
    """Update project input."""

    title = serializers.CharField(required=False)
    description = serializers.CharField(required=False)
    is_public = serializers.BooleanField(required=False)
    members = _ProjectMemberValidator(many=True, required=False)
    figma_integration = FigmaIntegrationDtoValidator(
        allow_null=True,
        required=False,
    )

    github_integration = GitHubIntegrationDtoValidator(
        allow_null=True,
        required=False,
    )

    gitlab_integration = GitLabIntegrationDtoValidator(
        allow_null=True,
        required=False,
    )
    emblem = serializers.PrimaryKeyRelatedField(
        queryset=Image.objects,
        required=False,
    )
    public_role = serializers.ChoiceField(
        choices=ProjectMemberRole.choices,
        required=False,
    )
    public_permissions = BitField(
        choices=ProjectPermission.choices,
        required=False,
    )
