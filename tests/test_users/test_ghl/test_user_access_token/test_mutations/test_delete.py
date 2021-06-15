from jnt_django_graphene_toolbox.errors import (
    GraphQLInputError,
    GraphQLPermissionDenied,
)

from apps.users.models import UserAccessToken
from tests.test_users.factories.user_access_token import UserAccessTokenFactory


def test_query(user, user_access_token, ghl_client, ghl_raw):
    """Test delete access token."""
    ghl_client.set_user(user)

    response = ghl_client.execute(
        ghl_raw("delete_access_token"),
        variable_values={
            "id": user_access_token.pk,
        },
    )

    assert "errors" not in response
    assert response["data"]["deleteAccessToken"]["status"] == "success"
    assert not user.access_tokens.exists()


def test_success(
    user,
    user_access_token,
    ghl_auth_mock_info,
    delete_access_token_mutation,
):
    """Test success delete access token."""
    response = delete_access_token_mutation(
        root=None,
        info=ghl_auth_mock_info,
        id=user_access_token.pk,
    )

    assert response.status == "success"
    assert not user.access_tokens.exists()


def test_remove_not_auth(
    user,
    user_access_token,
    ghl_mock_info,
    delete_access_token_mutation,
):
    """Test raise permissions denied."""
    response = delete_access_token_mutation(
        root=None,
        info=ghl_mock_info,
        id=user_access_token.pk,
    )

    assert isinstance(response, GraphQLPermissionDenied)
    assert user.access_tokens.first() == user_access_token


def test_remove_twice(
    user,
    user_access_token,
    ghl_auth_mock_info,
    delete_access_token_mutation,
):
    """Test twice delete access token."""
    access_token_pk = user_access_token.pk
    response = delete_access_token_mutation(
        root=None,
        info=ghl_auth_mock_info,
        id=access_token_pk,
    )

    assert response.status == "success"
    assert not user.access_tokens.exists()

    response_twice = delete_access_token_mutation(
        root=None,
        info=ghl_auth_mock_info,
        id=access_token_pk,
    )

    assert isinstance(response_twice, GraphQLInputError)


def test_delete_not_exists_token(
    user,
    user_access_token,
    ghl_auth_mock_info,
    delete_access_token_mutation,
):
    """Test delete not exists access token."""
    response = delete_access_token_mutation(
        root=None,
        info=ghl_auth_mock_info,
        id=0,
    )
    assert isinstance(response, GraphQLInputError)


def test_remove_not_self(
    user,
    ghl_auth_mock_info,
    delete_access_token_mutation,
):
    """Test delete not self token."""
    another_token = UserAccessTokenFactory.create()
    response = delete_access_token_mutation(
        root=None,
        info=ghl_auth_mock_info,
        id=another_token.pk,
    )

    assert isinstance(response, GraphQLPermissionDenied)
    assert UserAccessToken.objects.filter(pk=another_token.pk).exists()
