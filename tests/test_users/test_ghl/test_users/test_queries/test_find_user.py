import pytest
from jnt_django_graphene_toolbox.errors import GraphQLPermissionDenied

from tests.test_media.factories.image import ImageFactory
from tests.test_users.factories.user import UserFactory

FIND_EMAIL = "find_user@mail.com"


@pytest.fixture()
def find_user(db):
    """Create user for find."""
    return UserFactory.create(email=FIND_EMAIL)


def test_query(user, find_user, ghl_client, ghl_raw):
    """Test find user raw query."""
    ghl_client.set_user(user)

    response = ghl_client.execute(
        ghl_raw("find_user"),
        variable_values={"email": FIND_EMAIL},
    )

    assert "errors" not in response
    response_user = response["data"]["user"]
    assert response_user["id"] == str(find_user.id)


def test_unauth(ghl_client, find_user, ghl_raw):
    """Test unauth query."""
    response = ghl_client.execute(
        ghl_raw("find_user"),
        variable_values={"email": FIND_EMAIL},
    )

    assert "errors" in response
    assert len(response["errors"]) == 1
    error = response["errors"][0]

    assert error["message"] == str(GraphQLPermissionDenied().message)


def test_retrieve_with_avatar(user, find_user, ghl_client, ghl_raw):
    """Test retrieve avatar."""
    ghl_client.set_user(user)
    find_user.avatar = ImageFactory.create()
    find_user.save()

    response = ghl_client.execute(
        ghl_raw("find_user"),
        variable_values={"email": FIND_EMAIL},
    )
    assert "errors" not in response

    response_user = response["data"]["user"]

    assert response_user["id"] == str(find_user.id)
    assert response_user["avatar"]["id"] == str(find_user.avatar.id)


def test_resolver(user, find_user, ghl_auth_mock_info, find_user_query):
    """Test resolver query."""
    response = find_user_query(None, info=ghl_auth_mock_info, email=FIND_EMAIL)

    assert response == find_user


def test_user_not_found(user, ghl_auth_mock_info, find_user_query):
    """Test user not found."""
    response = find_user_query(None, info=ghl_auth_mock_info, email=FIND_EMAIL)

    assert response is None


def test_find_not_active(user, find_user, ghl_auth_mock_info, find_user_query):
    """Test find not active user."""
    find_user.is_active = False
    find_user.save()

    response = find_user_query(None, info=ghl_auth_mock_info, email=FIND_EMAIL)

    assert response is None
