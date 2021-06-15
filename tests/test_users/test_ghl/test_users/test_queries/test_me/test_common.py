from tests.test_media.factories.image import ImageFactory
from tests.test_users.factories.user_access_token import UserAccessTokenFactory


def test_query(user, ghl_client, ghl_raw):
    """Test me raw query."""
    ghl_client.set_user(user)

    response = ghl_client.execute(ghl_raw("me"))

    assert "errors" not in response
    assert response["data"]["me"]["id"] == str(user.id)


def test_unauth(ghl_client, ghl_raw):
    """Test unauth query."""
    response = ghl_client.execute(ghl_raw("me"))

    assert "errors" not in response
    assert response["data"]["me"] is None


def test_retrieve_avatar(user, ghl_client, ghl_raw):
    """Test retrieve avatar."""
    ghl_client.set_user(user)
    user.avatar = ImageFactory.create(created_by=user)
    user.save()

    response = ghl_client.execute(ghl_raw("me"))
    assert "errors" not in response

    me_response = response["data"]["me"]

    assert me_response["id"] == str(user.id)
    assert me_response["avatar"]["id"] == str(user.avatar.id)


def test_resolver(user, ghl_auth_mock_info, me_query):
    """Test me query."""
    response = me_query(None, info=ghl_auth_mock_info)

    assert response == user


def test_retrieve_access_tokens(user, ghl_client, ghl_raw):
    """Test retrieve access tokens."""
    access_token = UserAccessTokenFactory.create(user=user)
    ghl_client.set_user(user)

    response = ghl_client.execute(ghl_raw("me"))

    assert "errors" not in response
    assert response["data"]["me"]["id"] == str(user.id)
    response_tokens = response["data"]["me"]["accessTokens"]

    assert len(response_tokens) == 1
    assert response_tokens[0]["id"] == str(access_token.id)
    assert "key" not in response_tokens[0]
