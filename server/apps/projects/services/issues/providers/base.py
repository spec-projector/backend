from abc import ABC, abstractmethod

from apps.projects.graphql.types import IssueType


class BaseProvider(ABC):
    """Base provider."""

    def __init__(self, token: str) -> None:
        """Initializing."""
        self._token = token

    @abstractmethod
    def get_issue(self, url: str) -> IssueType:
        """Load issue."""
