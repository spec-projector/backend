# -*- coding: utf-8 -*-

GHL_QUERY_ME = """
query {
    me {
        id
        login
    }
}
"""


def test_query(user, ghl_client):
    """Test me raw query."""
    ghl_client.set_user(user)

    result = ghl_client.execute(GHL_QUERY_ME)

    assert 'errors' not in result
    assert result['data']['me']['id'] == str(user.id)


def test_resolver(user, ghl_auth_mock_info, me_query):
    """Test me query."""
    resolved = me_query(root=None, info=ghl_auth_mock_info)

    assert resolved == user
