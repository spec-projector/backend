from dataclasses import dataclass
from typing import Optional

from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext_lazy as _

from apps.core.logic.errors import BaseApplicationError
from apps.core.logic.use_cases import BaseUseCase
from apps.core.utils.date import seconds_to_hours
from apps.projects.graphql.types import AssigneeType
from apps.projects.services.issues.retriever import System, get_issue
from apps.projects.use_cases.issue.dto import InputDto, IssueDtoValidator

INTEGRATION_MAP = {  # noqa: WPS407
    System.GITHUB: "github_integration",
    System.GITLAB: "gitlab_integration",
}


class ProjectIntegrationNotFoundError(BaseApplicationError):
    """Project integration not found error."""

    code = "not_found"
    message = _("MSG__PROJECT_INTEGRATION_NOT_FOUND")


@dataclass(frozen=True)
class OutputDto:
    """Create issue output dto."""

    title: str
    state: Optional[str]
    due_date: str
    spent: int
    assignee: Optional[AssigneeType]


class UseCase(BaseUseCase):
    """Use case for retrieve issue."""

    def execute(self, input_dto: InputDto) -> OutputDto:
        """Main logic here."""
        validated_data = self.validate_input(
            input_dto,
            IssueDtoValidator,
        )

        issue_meta = get_issue(
            url=validated_data["url"],
            token=self._get_token(
                validated_data["project"],
                validated_data["system"],
            ),
            system=validated_data["system"],
        )

        assignee = None

        if issue_meta.assignee:
            assignee = AssigneeType(
                name=issue_meta.assignee.name,
                avatar=issue_meta.assignee.avatar,
            )

        spent = issue_meta.spent
        if spent:
            spent = seconds_to_hours(issue_meta.spent)

        return OutputDto(
            title=issue_meta.title,
            state=issue_meta.state.upper() if issue_meta.state else None,
            due_date=issue_meta.due_date,
            spent=spent,
            assignee=assignee,
        )

    def _get_token(self, project, system) -> str:
        """Getting integration token."""
        if system == System.DUMMY:
            return ""

        try:
            integration = getattr(project, INTEGRATION_MAP[system])
        except ObjectDoesNotExist:
            raise ProjectIntegrationNotFoundError()
        else:
            return integration.token
