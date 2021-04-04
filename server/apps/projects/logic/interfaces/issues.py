import abc
from dataclasses import dataclass
from enum import Enum
from typing import Optional

from apps.projects.models import Project


class IssuesManagementSystem(Enum):
    """Issues management system enum."""

    GITHUB = 1  # noqa: WPS115
    GITLAB = 2  # noqa: WPS115
    DUMMY = 3  # noqa: WPS115


@dataclass
class AssigneeMeta:
    """Assignee meta."""

    name: str
    avatar: str


@dataclass
class IssueMeta:
    """Issue meta."""

    title: str
    state: str
    due_date: Optional[str]
    spent: Optional[int]
    assignee: Optional[AssigneeMeta]


class IIssuesService(abc.ABC):
    """Issues service interface."""

    @abc.abstractmethod
    def get_issue_meta(
        self,
        url: str,
        project: Project,
        system: IssuesManagementSystem,
    ) -> IssueMeta:
        """Get issue meta from external system."""
