from typing import Optional, Union

import graphene
from graphql import ResolveInfo

from apps.projects.models import (
    FigmaIntegration,
    GitHubIntegration,
    GitLabIntegration,
)

Integration = Union[FigmaIntegration, GitHubIntegration, GitLabIntegration]


class BaseIntegrationType(graphene.ObjectType):
    """Base integration type."""

    token = graphene.String(required=True)

    def resolve_token(
        self: Integration,
        info: ResolveInfo,  # noqa: WPS110
    ) -> Optional[str]:
        """Resolve token integration."""
        return "*" if self.token else None
