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
