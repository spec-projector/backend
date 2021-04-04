from dataclasses import dataclass
from typing import Optional

import injector

from apps.core.logic.use_cases import BaseUseCase
from apps.core.utils.date import seconds_to_hours
from apps.projects.graphql.types import AssigneeType
from apps.projects.logic.interfaces import IIssuesService
from apps.projects.logic.use_cases.issue.dto import InputDto, IssueDtoValidator


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

    @injector.inject
    def __init__(self, issues_service: IIssuesService):
        """Initialize."""
        self._issues_service = issues_service

    def execute(self, input_dto: InputDto) -> OutputDto:
        """Main logic here."""
        validated_data = self.validate_input(
            input_dto,
            IssueDtoValidator,
        )

        issue_meta = self._issues_service.get_issue_meta(
            url=validated_data["url"],
            project=validated_data["project"],
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
