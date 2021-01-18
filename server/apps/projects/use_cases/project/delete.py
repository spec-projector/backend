from dataclasses import dataclass

from rest_framework import serializers

from apps.core.application.use_cases import BasePresenter, BaseUseCase
from apps.projects.models import Project
from apps.users.models import User


@dataclass(frozen=True)
class ProjectDeleteData:
    """Delete project data."""

    project: int


@dataclass(frozen=True)
class InputDto:
    """Delete project input dto."""

    data: ProjectDeleteData  # noqa: WPS110
    user: User


class InputDtoValidator(serializers.Serializer):
    """Delete project input."""

    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects)


class UseCase(BaseUseCase):
    """Use case for deleting projects."""

    def __init__(self, presenter: BasePresenter):
        """Initialize."""
        self._presenter = presenter

    def execute(self, input_dto: InputDto) -> None:
        """Main logic here."""
        validated_data = self.validate_input(
            input_dto.data,
            InputDtoValidator,
        )
        validated_data["project"].delete()
