from graphql import ResolveInfo

from apps.projects.logic.use_cases.issue.dto import InputDto
from apps.projects.logic.use_cases.issue.retrieve import OutputDto, UseCase
from apps.projects.services.issues.meta import System


def resolve_issue(
    parent,
    info: ResolveInfo,  # noqa: WPS110
    input,  # noqa: WPS125
) -> OutputDto:
    """Resolve issue."""
    input_dto = InputDto(
        project=input.project,
        url=input.url,
        system=System(input.system),
    )

    return UseCase().execute(input_dto)
