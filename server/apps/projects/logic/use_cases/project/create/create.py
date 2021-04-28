import injector

from apps.billing.logic.interfaces import ITariffLimitsService
from apps.core.logic.helpers.validation import validate_input
from apps.core.logic.interfaces import ICouchDBService
from apps.core.logic.use_cases import BaseUseCase
from apps.core.utils.objects import empty
from apps.projects.logic.use_cases.project.create.dto import (
    InputDto,
    OutputDto,
    ProjectDtoValidator,
)
from apps.projects.models import (
    FigmaIntegration,
    GitHubIntegration,
    GitLabIntegration,
    Project,
)


class UseCase(BaseUseCase):
    """Use case for creating projects."""

    @injector.inject
    def __init__(
        self,
        tariff_limits_service: ITariffLimitsService,
        couch_db_service: ICouchDBService,
    ):
        """Initialize."""
        self._tariff_limits_service = tariff_limits_service
        self._couch_db_service = couch_db_service

    def execute(self, input_dto: InputDto) -> OutputDto:
        """Main logic here."""
        validated_data = validate_input(
            input_dto.data,
            ProjectDtoValidator,
        )
        self._tariff_limits_service.assert_new_project_allowed(input_dto.user)

        project = Project.objects.create(
            title=validated_data["title"],
            is_public=validated_data["is_public"],
            description=validated_data["description"],
            owner=input_dto.user,
        )

        self._add_figma_integration(project, validated_data)
        self._add_github_integration(project, validated_data)
        self._add_gitlab_integration(project, validated_data)

        self._couch_db_service.create_database(project.db_name)

        return OutputDto(project=project)

    def _add_figma_integration(self, project: Project, validated_data) -> None:
        integration = validated_data.get("figma_integration")
        if integration and integration != empty:
            FigmaIntegration.objects.create(
                project=project,
                token=integration["token"],
            )

    def _add_github_integration(
        self,
        project: Project,
        validated_data,
    ) -> None:
        integration = validated_data.get("github_integration")
        if integration and integration != empty:
            GitHubIntegration.objects.create(
                project=project,
                token=integration["token"],
            )

    def _add_gitlab_integration(
        self,
        project: Project,
        validated_data,
    ) -> None:
        integration = validated_data.get("gitlab_integration")
        if integration and integration != empty:
            GitLabIntegration.objects.create(
                project=project,
                token=integration["token"],
            )
