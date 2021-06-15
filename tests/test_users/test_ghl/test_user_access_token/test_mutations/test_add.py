from jnt_django_graphene_toolbox.errors import GraphQLPermissionDenied

from apps.users.models import UserAccessToken

ACCESS_TOKEN_NAME = "api access"  # noqa: S105


def test_query(user, ghl_client, ghl_raw):
    """Test add access token."""
    ghl_client.set_user(user)

    response = ghl_client.execute(
        ghl_raw("add_access_token"),
        variable_values={
            "name": ACCESS_TOKEN_NAME,
        },
    )

    assert "errors" not in response
    access_token = user.access_tokens.get(name=ACCESS_TOKEN_NAME)
    response_token = response["data"]["addAccessToken"]["accessToken"]
    assert response_token["key"] == access_token.key


def test_success(user, ghl_auth_mock_info, add_access_token_mutation):
    """Test success add access token."""
    response = add_access_token_mutation(
        root=None,
        info=ghl_auth_mock_info,
        name=ACCESS_TOKEN_NAME,
    )

    user_token = user.access_tokens.first()
    assert response.access_token["id"] == user_token.id
    assert response.access_token["key"] == user_token.key
    assert response.access_token["name"] == ACCESS_TOKEN_NAME


def test_add_twice(user, ghl_auth_mock_info, add_access_token_mutation):
    """Test add access token twice."""
    add_access_token_mutation(
        root=None,
        info=ghl_auth_mock_info,
        name=ACCESS_TOKEN_NAME,
    )
    add_access_token_mutation(
        root=None,
        info=ghl_auth_mock_info,
        name=ACCESS_TOKEN_NAME,
    )

    assert user.access_tokens.count() == 2
    assert user.access_tokens.filter(name=ACCESS_TOKEN_NAME).count() == 2


def test_not_auth(user, ghl_mock_info, add_access_token_mutation):
    """Test add user access token not auth."""
    response = add_access_token_mutation(
        root=None,
        info=ghl_mock_info,
        name=ACCESS_TOKEN_NAME,
    )
    assert isinstance(response, GraphQLPermissionDenied)
    assert not UserAccessToken.objects.exists()
