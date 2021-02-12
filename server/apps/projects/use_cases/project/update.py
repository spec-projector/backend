from dataclasses import dataclass
from typing import List, Type, Union

from django.db import models
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.core.application.use_cases import BaseUseCase
from apps.core.serializers.fields import BitField
from apps.core.utils.objects import Empty, empty
from apps.projects.models import (
    FigmaIntegration,
    GitHubIntegration,
    GitLabIntegration,
    Project,
)
from apps.projects.models.project_member import (
    ProjectMember,
    ProjectMemberRole,
)
from apps.projects.use_cases.project.dto import (
    FigmaIntegrationDto,
    FigmaIntegrationDtoValidator,
    GitHubIntegrationDto,
    GitHubIntegrationDtoValidator,
    GitLabIntegrationDto,
    GitLabIntegrationDtoValidator,
)
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
    users: List[ProjectMemberDto] = empty


@dataclass(frozen=True)
class InputDto:
    """Update project input dto."""

    data: ProjectDto  # noqa: WPS110
    project: int
    user: User


@dataclass(frozen=True)
class OutputDto:
    """Update project output dto."""

    project: Project


class ProjectMemberValidator(serializers.Serializer):
    """Project member serializer."""

    id = serializers.PrimaryKeyRelatedField(  # noqa: WPS125
        queryset=User.objects,
    )
    roles = BitField(choices=ProjectMemberRole.choices)

    def validate_roles(self, roles):
        """Roles validation."""
        if not roles:
            raise ValidationError("Roles not set")
        return roles


class ProjectDtoValidator(serializers.Serializer):
    """Update project input."""

    title = serializers.CharField(required=False)
    description = serializers.CharField(required=False)
    is_public = serializers.BooleanField(required=False)
    users = ProjectMemberValidator(many=True, required=False)
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


class UseCase(BaseUseCase):
    """Use case for updating projects."""

    def execute(self, input_dto: InputDto) -> OutputDto:
        """Main logic here."""
        project = Project.objects.filter(pk=input_dto.project).first()
        if not project:
            raise ValidationError("Project not found")

        validated_data = self.validate_input(
            input_dto.data,
            ProjectDtoValidator,
        )
        members = validated_data.pop("users", None)
        if members is not None:
            self._update_members(project, members)

        self._update_figma_integration(project, validated_data)
        self._update_github_integration(project, validated_data)
        self._update_gitlab_integration(project, validated_data)

        for field, field_value in validated_data.items():
            setattr(project, field, field_value)
        project.save()

        return OutputDto(project=project)

    def _update_members(self, project, members) -> None:
        project_members = []
        for project_member_input in members:
            project_member, _ = ProjectMember.objects.update_or_create(
                project=project,
                user=project_member_input["id"],
                defaults={"roles": project_member_input.get("roles")},
            )

            project_members.append(project_member)

        for member in ProjectMember.objects.filter(project=project):
            if member not in project_members:
                member.delete()

    def _update_figma_integration(
        self,
        project: Project,
        validated_data,
    ) -> None:
        self._update_integration(
            project,
            validated_data,
            FigmaIntegration,
            "figma_integration",
        )

    def _update_github_integration(
        self,
        project: Project,
        validated_data,
    ) -> None:
        self._update_integration(
            project,
            validated_data,
            GitHubIntegration,
            "github_integration",
        )

    def _update_gitlab_integration(
        self,
        project: Project,
        validated_data,
    ) -> None:
        self._update_integration(
            project,
            validated_data,
            GitLabIntegration,
            "gitlab_integration",
        )

    def _update_integration(
        self,
        project: Project,
        validated_data,
        model: Type[models.Model],
        field: str,
    ):
        integration_dto = validated_data.pop(field, empty)
        if integration_dto != empty:
            if integration_dto:
                model.objects.update_or_create(
                    project=project,
                    defaults={"token": integration_dto["token"]},
                )
            else:
                model.objects.filter(project=project).delete()
