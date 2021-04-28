import injector

from apps.billing.logic.interfaces import (
    ISubscriptionService,
    IUserTariffService,
)
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
        subscription_service: ISubscriptionService,
        user_tariff_service: IUserTariffService,
        couch_db_service: ICouchDBService,
    ):
        """Initialize."""
        self._subscription_service = subscription_service
        self._user_tariff_service = user_tariff_service
        self._couch_db_service = couch_db_service

    def execute(self, input_dto: InputDto) -> OutputDto:
        """Main logic here."""
        validated_data = validate_input(
            input_dto.data,
            ProjectDtoValidator,
        )

        self._user_tariff_service.validate_max_projects(
            self._subscription_service.get_user_subscription(
                input_dto.user,
            ),
            Project.objects.filter(owner=input_dto.user).count() + 1,
        )

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
