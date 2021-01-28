from dataclasses import dataclass

from rest_framework import serializers

from apps.core import injector
from apps.core.application.use_cases import BasePresenter, BaseUseCase
from apps.core.services.couchdb import CouchDBService
from apps.projects.models import Project
from apps.users.models import User


@dataclass(frozen=True)
class ProjectCreateData:
    """Create project data."""

    title: str
    is_public: bool
    description: str


@dataclass(frozen=True)
class InputDto:
    """Create project input dto."""

    data: ProjectCreateData  # noqa: WPS110
    user: User


@dataclass(frozen=True)
class OutputDto:
    """Create project output dto."""

    project: Project


class InputDtoValidator(serializers.Serializer):
    """Create project input."""

    title = serializers.CharField()
    is_public = serializers.BooleanField(default=False)
    description = serializers.CharField(default="", allow_blank=True)


class UseCase(BaseUseCase):
    """Use case for creating projects."""

    def __init__(self, presenter: BasePresenter):
        """Initialize."""
        self._presenter = presenter

    def execute(self, input_dto: InputDto) -> None:
        """Main logic here."""
        validated_data = self.validate_input(
            input_dto.data,
            InputDtoValidator,
        )
        project = Project.objects.create(
            title=validated_data["title"],
            is_public=validated_data["is_public"],
            description=validated_data["description"],
            owner=input_dto.user,
        )

        couch_db = injector.get(CouchDBService)
        couch_db.create_database(project.db_name)
        couch_db.close()

        self._presenter.present(OutputDto(project=project))
