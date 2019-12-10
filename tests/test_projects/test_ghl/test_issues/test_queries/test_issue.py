# -*- coding: utf-8 -*-

GHL_QUERY_ISSUE = """
{{
  issue(url: "{0}", token: "{1}", system: {2}) {{
    status
    title
  }}
}}
"""


def test_query(user, ghl_client):
    """Test getting issue raw query."""
    ghl_client.set_user(user)

    response = ghl_client.execute(
        GHL_QUERY_ISSUE.format('https://dummy.com', 'dummy_token', 'DUMMY'),
    )

    assert 'errors' not in response
    assert response['data']['issue']['title'] is None
    assert response['data']['issue']['status'] is None


def test_gitlab_issue(user, ghl_client, gl_mocker):
    """Test getting gitlab issue."""
    gl_issue = {
        'title': 'Test issue',
        'state': 'opened',
        'id': 44,
        'iid': 33,
    }

    gl_mocker.registry_get('/projects/test-project/issues/33', gl_issue)

    ghl_client.set_user(user)

    response = ghl_client.execute(
        GHL_QUERY_ISSUE.format(
            'https://gitlab.com/test-project/issues/33',
            'GITLAB_TOKEN',
            'GITLAB',
        ),
    )

    assert 'errors' not in response
    assert response['data']['issue']['title'] == gl_issue['title']
    assert response['data']['issue']['status'] == gl_issue['state']
