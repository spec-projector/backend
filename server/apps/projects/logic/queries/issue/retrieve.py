from dataclasses import dataclass
from typing import Optional

import injector
from rest_framework import serializers

from apps.core.logic import queries
from apps.core.logic.helpers.validation import validate_input
from apps.core.utils.date import seconds_to_hours
from apps.projects.graphql.types import AssigneeType
from apps.projects.logic.interfaces.issues import (
    IIssuesService,
    IssuesManagementSystem,
)
from apps.projects.models import Project


@dataclass(frozen=True)
class GetIssueQuery(queries.IQuery):
    """Create issue input dto."""

    project: str
    url: str
    system: IssuesManagementSystem


@dataclass(frozen=True)
class Issue:
    """Create issue output dto."""

    title: str
    state: Optional[str]
    due_date: str
    spent: int
    assignee: Optional[AssigneeType]


class _InputDtoValidator(serializers.Serializer):
    """Create issue input dto validator."""

    project = serializers.PrimaryKeyRelatedField(
        queryset=Project.objects.all(),
    )
    url = serializers.CharField()
    system = serializers.ChoiceField(choices=IssuesManagementSystem)


class QueryHandler(queries.IQueryHandler[GetIssueQuery, Issue]):
    """Get issue from external system."""

    @injector.inject
    def __init__(self, issues_service: IIssuesService):
        """Initialize."""
        self._issues_service = issues_service

    def ask(self, query: GetIssueQuery) -> Issue:
        """Handler."""
        validated_data = validate_input(query, _InputDtoValidator)

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

        return Issue(
            title=issue_meta.title,
            state=issue_meta.state.upper() if issue_meta.state else None,
            due_date=issue_meta.due_date,
            spent=spent,
            assignee=assignee,
        )
