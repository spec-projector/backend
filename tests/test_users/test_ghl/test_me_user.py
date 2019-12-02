# -*- coding: utf-8 -*-

from apps.users.graphql.resolvers import resolve_me_user

GHL_QUERY_ME = """
query {
    me {
        id
      	login
    }
}
"""


def test_query(user, ghl_client):
    """Test me query."""
    ghl_client.set_user(user)

    result = ghl_client.execute(GHL_QUERY_ME)

    assert 'errors' not in result
    assert result['data']['me']['id'] == str(user.id)


def test_resolver(user, ghl_auth_mock_info):
    """Test me resolver."""
    resolved_user = resolve_me_user(None, ghl_auth_mock_info)

    assert resolved_user == user
