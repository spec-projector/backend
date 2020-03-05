# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod

from apps.projects.graphql.types import IssueType


class BaseProvider(ABC):
    """Base provider."""

    def __init__(self, url: str, token: str) -> None:
        """Initializing."""
        self._url = url
        self._token = token

    @abstractmethod
    def get_issue(self) -> IssueType:
        """Load issue."""
