# -*- coding: utf-8 -*-

import pytest

from apps.projects.services.issues.providers import GitlabProvider


@pytest.fixture()
def provider():
    """Provide gitlab provider."""
    return GitlabProvider("GITLAB_TOKEN")


@pytest.fixture()
def gl_issue():
    """Provide gitlab issue mock."""
    return {
        "title": "Test issue",
        "state": "OPENED",
        "due_date": "2015-10-08",
        "time_stats": {
            "time_estimate": 3600,
            "total_time_spent": 3600,
            "human_time_estimate": "1h",
            "human_total_time_spent": "1h",
        },
        "assignee": None,
    }


def test_success(provider, gl_mocker, gl_issue):
    """Test success issue retrieving."""
    gl_mocker.register_get("/projects/test-project/issues/33", gl_issue)

    issue = provider.get_issue("https://gitlab.com/test-project/issues/33")
    assert issue.title == gl_issue["title"]


def test_path_with_dash(provider, gl_mocker, gl_issue):
    """Test if issue path contains '-' segment."""
    gl_mocker.register_get("/projects/test-project/issues/33", gl_issue)

    issue = provider.get_issue("https://gitlab.com/test-project/-/issues/33")
    assert issue.title == gl_issue["title"]
