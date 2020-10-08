import re
from typing import Optional, Tuple

from django.conf import settings
from django.utils.translation import gettext_lazy as _
from github import Github, Issue
from rest_framework.exceptions import ValidationError

from apps.projects.services.issues.meta import AssigneeMeta, IssueMeta
from apps.projects.services.issues.providers.base import BaseProvider


class GithubProvider(BaseProvider):
    """Github provider."""

    def get_issue(self, url: str) -> IssueMeta:
        """Load issue."""
        gh_issue = self._get_github_issue(url)

        return IssueMeta(
            title=gh_issue.title,  # type: ignore
            state=gh_issue.state,  # type: ignore
            assignee=self._get_assignee(gh_issue),
            spent=None,
            due_date=None,
        )

    def _get_github_issue(self, url: str) -> Issue:  # type: ignore
        gh_client = self._get_github_client()
        owner, project, issue_number = self._parse_url(url)

        repository = gh_client.get_repo("{0}/{1}".format(owner, project))

        return repository.get_issue(number=int(issue_number))

    def _get_github_client(self) -> Github:
        return Github(self._token, base_url=settings.GITHUB_HOST)

    def _parse_url(self, url: str) -> Tuple[str, str, str]:
        pattern = r"/(\w+)/(\w+)/issues/(\d+)"
        issue_data = re.findall(pattern, url)

        if not issue_data:
            raise ValidationError(_("MSG_GITHUB_ISSUE_URL_NOT_VALID"))

        return issue_data[0]

    def _get_assignee(
        self,
        issue: Issue,  # type: ignore
    ) -> Optional[AssigneeMeta]:
        if issue.assignee:  # type: ignore
            return AssigneeMeta(
                name=issue.assignee.name,  # type: ignore
                avatar=issue.assignee.avatar_url,  # type: ignore
            )

        return None
