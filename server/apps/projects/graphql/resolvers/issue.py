from graphql import ResolveInfo

from apps.core import injector
from apps.projects.logic.interfaces.issues import IssuesManagementSystem
from apps.projects.logic.use_cases.issue.dto import InputDto
from apps.projects.logic.use_cases.issue.retrieve import OutputDto, UseCase


def resolve_issue(
    parent,
    info: ResolveInfo,  # noqa: WPS110
    input,  # noqa: WPS125
) -> OutputDto:
    """Resolve issue."""
    return injector.get(UseCase).execute(
        InputDto(
            project=input.project,
            url=input.url,
            system=IssuesManagementSystem(input.system),
        ),
    )
