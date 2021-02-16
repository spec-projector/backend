from typing import Optional, Union

from graphql import ResolveInfo

from apps.projects.models import (
    FigmaIntegration,
    GitHubIntegration,
    GitLabIntegration,
)

Integration = Union[FigmaIntegration, GitHubIntegration, GitLabIntegration]


def resolve_token_integration(
    integration: Integration,
    info: ResolveInfo,  # noqa: WPS110
    **kwargs,
) -> Optional[str]:
    """Resolve token integration."""
    return "*" if integration.token else None
