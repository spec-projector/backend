# -*- coding: utf-8 -*-

import re
from typing import Tuple

from django.conf import settings
from django.utils.translation import gettext_lazy as _
from github import Github, Issue
from rest_framework.exceptions import ValidationError

from apps.projects.graphql.types import IssueType
from apps.projects.services.issues.providers.base import BaseProvider


class GithubProvider(BaseProvider):
    """Github provider."""

    def get_issue(self) -> IssueType:
        gh_issue = self._get_github_issue()

        return IssueType(
            title=gh_issue.title,
            status=gh_issue.state,
        )

    def _get_github_issue(self) -> Issue:
        gh_client = self._get_github_client()
        owner, project, issue_number = self._parse_url()

        repository = gh_client.get_repo('{0}/{1}'.format(owner, project))

        return repository.get_issue(number=int(issue_number))

    def _get_github_client(self) -> Github:
        return Github(self._token, base_url=settings.GITHUB_HOST)

    def _parse_url(self) -> Tuple[str, str, str]:
        pattern = r'/(\w+)/(\w+)/issues/(\d+)'
        issue_data = re.findall(pattern, self._url)

        if not issue_data:
            raise ValidationError(_('MSG_GITHUB_ISSUE_URL_NOT_VALID'))

        return issue_data[0]
