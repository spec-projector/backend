# -*- coding: utf-8 -*-

from apps.projects.services.issues.retriever import System

GHL_QUERY_ISSUE = """
query ($url: String!, $token: String!, $system: System!) {
  issue(url: $url, token: $token, system: $system) {
    title
    state
    dueDate
    spent
    assignee {
      name
      avatar
    }
  }
}
"""


def test_query(user, ghl_client):
    """Test getting issue raw query."""
    ghl_client.set_user(user)

    response = ghl_client.execute(
        GHL_QUERY_ISSUE,
        variable_values={
            "url": "https://dummy.com",
            "token": "dummy_token",
            "system": System.DUMMY.name,
        },
    )

    assert "errors" not in response
    assert response["data"]["issue"]["title"] is None
    assert response["data"]["issue"]["state"] is None


def test_gitlab_issue(user, ghl_client, gl_mocker):
    """Test getting gitlab issue."""
    gl_issue = {
        "title": "Test issue",
        "state": "OPENED",
        "id": 44,
        "iid": 33,
        "due_date": "2015-10-08",
        "assignee": {
            "name": "Joe",
            "avatar_url": "https://images.com/image/23",
        },
        "time_stats": {
            "time_estimate": 3600,
            "total_time_spent": 3600,
            "human_time_estimate": "1h",
            "human_total_time_spent": "1h",
        },
    }

    gl_mocker.register_get("/projects/test-project/issues/33", gl_issue)

    ghl_client.set_user(user)

    response = ghl_client.execute(
        GHL_QUERY_ISSUE,
        variable_values={
            "url": "https://gitlab.com/test-project/issues/33",
            "token": "GITLAB_TOKEN",
            "system": System.GITLAB.name,
        },
    )

    issue = response["data"]["issue"]
    assignee = response["data"]["issue"]["assignee"]

    assert issue["title"] == gl_issue["title"]
    assert issue["state"] == gl_issue["state"]
    assert issue["spent"] == 1.0
    assert assignee["name"] == gl_issue["assignee"]["name"]


def test_githab_issue(user, ghl_client, gh_mocker):
    """Test getting gitlab issue."""
    gh_repo = {
        "id": 12345,
        "name": "django_issue",
        "full_name": "owner/django_issue",
        "url": "https://api.github.com/repos/owner/django_issue",
    }

    gh_issue = {
        "title": "Test issue for check gpl",
        "state": "OPEN",
        "assignee": {
            "name": "Joe",
            "avatar_url": "https://images.com/image/23",
        },
    }

    gh_mocker.register_get("/repos/owner/django_issue", gh_repo)
    gh_mocker.register_get("/repos/owner/django_issue/issues/5", gh_issue)

    ghl_client.set_user(user)

    response = ghl_client.execute(
        GHL_QUERY_ISSUE,
        variable_values={
            "url": "https://github.com/owner/django_issue/issues/5",
            "token": "GITHUB_TOKEN",
            "system": System.GITHUB.name,
        },
    )

    issue = response["data"]["issue"]
    assignee = response["data"]["issue"]["assignee"]

    assert issue["title"] == gh_issue["title"]
    assert issue["state"] == gh_issue["state"]
    assert assignee["name"] == gh_issue["assignee"]["name"]
