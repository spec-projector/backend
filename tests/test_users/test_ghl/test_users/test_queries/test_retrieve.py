# -*- coding: utf-8 -*-

GHL_QUERY_USER = """
query {{
  user(id: {0}) {{
    id
    login
  }}
}}
"""


def test_query(user, ghl_client):
    """Test getting user raw query."""
    ghl_client.set_user(user)

    response = ghl_client.execute(GHL_QUERY_USER.format(user.id))

    assert 'errors' not in response
    assert response['data']['user']['id'] == str(user.id)


def test_success(user, ghl_auth_mock_info, user_query):
    """Test success user retrieving."""
    response = user_query(
        root=None,
        info=ghl_auth_mock_info,
        id=user.id,
    )

    assert response == user


def test_inactive(user, ghl_auth_mock_info, user_query):
    """Test success inactive user retrieving."""
    user.is_active = False
    user.save(update_fields=['is_active'])

    response = user_query(
        root=None,
        info=ghl_auth_mock_info,
        id=user.id,
    )

    assert response is None
