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
    """Test getting user query."""
    ghl_client.set_user(user)

    result = ghl_client.execute(GHL_QUERY_USER.format(user.id))

    assert 'errors' not in result
    assert result['data']['user']['id'] == str(user.id)


def test_success(user, ghl_auth_mock_info, user_resolver):
    """Test success user retrieving."""
    retrieved = user_resolver(
        root=None,
        info=ghl_auth_mock_info,
        id=user.id,
    )

    assert retrieved == user


def test_inactive(user, ghl_auth_mock_info, user_resolver):
    """Test success inactive user retrieving."""
    user.is_active = False
    user.save(update_fields=['is_active'])

    retrieved = user_resolver(
        root=None,
        info=ghl_auth_mock_info,
        id=user.id,
    )

    assert retrieved is None
