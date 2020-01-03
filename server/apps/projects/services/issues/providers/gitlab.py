# -*- coding: utf-8 -*-

from typing import Optional, Tuple
from urllib.parse import urlparse

import gitlab
from django.conf import settings
from gitlab.v4.objects import Issue

from apps.projects.services.issues.meta import AssigneeMeta, IssueMeta
from apps.projects.services.issues.providers.base import BaseProvider


class GitlabProvider(BaseProvider):
    """Gitlab provider."""

    def get_issue(self) -> IssueMeta:
        gl_issue = self._get_gitlab_issue()

        return IssueMeta(
            title=gl_issue.title,
            state=gl_issue.state,
            due_date=gl_issue.due_date,
            assignee=self._get_assignee(gl_issue),
            spent=gl_issue.time_stats().get("total_time_spent", 0),
        )

    def _get_gitlab_issue(self) -> Issue:
        """Getting gitlab issue."""
        gl_client = self._get_gitlab_client()
        project_id, issue_id = self._parse_url()

        project = gl_client.projects.get(project_id, lazy=True)

        return project.issues.get(issue_id)

    def _get_gitlab_client(self) -> gitlab.Gitlab:
        """Getting Gitlab client."""
        return gitlab.Gitlab(settings.GITLAB_HOST, self._token)

    def _parse_url(self) -> Tuple[str, str]:
        """Getting project id and issue id."""
        parts = [part for part in urlparse(self._url).path.split("/") if part]

        project_id = "/".join(parts[:-2])
        issue_id = parts[-1:][0]

        return project_id, issue_id

    def _get_assignee(self, issue: Issue) -> Optional[AssigneeMeta]:
        if issue.assignee:
            return AssigneeMeta(
                name=issue.assignee["name"],
                avatar=issue.assignee["avatar_url"],
            )
        return None
