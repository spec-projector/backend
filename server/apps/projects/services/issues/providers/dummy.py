# -*- coding: utf-8 -*-

from apps.projects.graphql.types import IssueType
from apps.projects.services.issues.providers.base import BaseProvider


class DummyProvider(BaseProvider):
    """Dummy provider."""

    def get_issue(self, url: str) -> IssueType:
        """Load issue."""
        return IssueType()
