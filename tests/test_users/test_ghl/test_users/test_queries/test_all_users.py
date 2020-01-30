# -*- coding: utf-8 -*-

from tests.test_users.factories.user import UserFactory

GHL_QUERY_ALL_USERS = """
query ($email: String) {
    allUsers(email: $email) {
      edges {
        node {
          id
          login
        }
      }
    }
  }
"""


def test_query(user, ghl_client):
    """Test getting all users raw query."""
    ghl_client.set_user(user)

    response = ghl_client.execute(
        GHL_QUERY_ALL_USERS,
    )

    assert "errors" not in response

    edges = response["data"]["allUsers"]["edges"]

    assert len(edges) == 1
    assert edges[0]["node"]["id"] == str(user.id)


def test_success(user, ghl_auth_mock_info, all_users_query):
    """Test success all users retrieving."""
    response = all_users_query(
        root=None,
        info=ghl_auth_mock_info,
    )

    assert response.length == 1
    assert response.edges[0].node == user


def test_inactive(user, ghl_auth_mock_info, all_users_query):
    """Test success inactive all users retrieving."""
    user.is_active = False
    user.save(update_fields=["is_active"])

    response = all_users_query(
        root=None,
        info=ghl_auth_mock_info,
    )

    assert not response.length


def test_email_filter(user, ghl_auth_mock_info, all_users_query):
    """Test filter users by email."""
    email = "test@test.it"
    user1 = UserFactory.create(is_active=True, email=email)

    response = all_users_query(
        root=None,
        info=ghl_auth_mock_info,
        email=email,
    )

    assert response.length == 1
    assert response.edges[0].node == user1


def test_email_filter_not_found(user, ghl_auth_mock_info, all_users_query):
    """Test filter users by email not found."""
    UserFactory.create(is_active=True)

    response = all_users_query(
        root=None,
        info=ghl_auth_mock_info,
        email="unique-test@test.it",
    )

    assert not response.length
