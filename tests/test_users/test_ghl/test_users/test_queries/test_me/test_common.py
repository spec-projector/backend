def test_query(user, ghl_client, ghl_raw):
    """Test me raw query."""
    ghl_client.set_user(user)

    response = ghl_client.execute(ghl_raw("me"))

    assert response["data"]["me"]["id"] == str(user.id)


def test_unauth(ghl_client, ghl_raw):
    """Test unauth query."""
    response = ghl_client.execute(ghl_raw("me"))

    assert "errors" in response


def test_resolver(user, ghl_auth_mock_info, me_query):
    """Test me query."""
    response = me_query(None, info=ghl_auth_mock_info)

    assert response == user
