from dataclasses import dataclass
from typing import List

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.core.application.use_cases import BasePresenter, BaseUseCase
from apps.core.serializers.fields import BitField
from apps.projects.models import Project
from apps.projects.models.project_member import (
    ProjectMember,
    ProjectMemberRole,
)
from apps.users.models import User


@dataclass(frozen=True)
class ProjectMemberData:
    """Update project member data."""

    user: int
    roles: int


@dataclass(frozen=True)
class ProjectUpdateData:
    """Update project data."""

    project: int
    title: str
    description: str
    is_public: bool
    users: List[ProjectMemberData]


@dataclass(frozen=True)
class InputDto:
    """Update project input dto."""

    data: ProjectUpdateData  # noqa: WPS110
    user: User


@dataclass(frozen=True)
class OutputDto:
    """Update project output dto."""

    project: Project


class _ProjectMember(serializers.Serializer):
    """Project member serializer."""

    id = serializers.PrimaryKeyRelatedField(  # noqa: A003, WPS125
        queryset=User.objects,
    )
    roles = BitField(choices=ProjectMemberRole.choices)

    def validate_roles(self, roles):
        """Roles validation."""
        if not roles:
            raise ValidationError("Roles not set")
        return roles


class InputDtoValidator(serializers.Serializer):
    """Update project input."""

    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects)
    title = serializers.CharField(required=False)
    description = serializers.CharField(required=False)
    is_public = serializers.BooleanField(required=False)
    users = _ProjectMember(many=True, required=False)


class UseCase(BaseUseCase):
    """Use case for updating projects."""

    def __init__(self, presenter: BasePresenter):
        """Initialize."""
        self._presenter = presenter

    def execute(self, input_dto: InputDto) -> None:
        """Main logic here."""
        validated_data = self.validate_input(
            input_dto.data,
            InputDtoValidator,
        )
        project = validated_data["project"]
        members = validated_data.pop("users", None)
        if members is not None:
            self._update_members(project, members)

        for field, field_value in validated_data.items():
            setattr(project, field, field_value)
        project.save()

        self._presenter.present(OutputDto(project=project))

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
