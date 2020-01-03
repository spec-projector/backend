# -*- coding: utf-8 -*-

from pytest import raises
from rest_framework.exceptions import PermissionDenied

from tests.test_projects.factories.project import ProjectFactory

GHL_QUERY_ALL_PROJECTS = """
query {
  allProjects {
    count
    edges{
      node{
        id
      }
    }
  }
}
"""


def test_query(user, ghl_client):
    """Test getting all projects raw query."""
    ghl_client.set_user(user)

    ProjectFactory.create_batch(5, owner=user)

    response = ghl_client.execute(GHL_QUERY_ALL_PROJECTS)

    assert "errors" not in response
    assert response["data"]["allProjects"]["count"] == 5


def test_success(ghl_auth_mock_info, all_projects_query):
    """Test success list project."""
    ProjectFactory.create_batch(5, owner=ghl_auth_mock_info.context.user)
    response = all_projects_query(
        root=None,
        info=ghl_auth_mock_info,
    )

    assert response.length == 5


def test_unauth(ghl_mock_info, all_projects_query):
    """Test unauth list project access."""
    ProjectFactory.create_batch(5)

    with raises(PermissionDenied):
        all_projects_query(
            root=None,
            info=ghl_mock_info,
        )
