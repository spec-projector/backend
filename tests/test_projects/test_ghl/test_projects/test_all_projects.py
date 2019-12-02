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
    """Test getting all projects query."""
    ghl_client.set_user(user)

    ProjectFactory.create_batch(5)

    result = ghl_client.execute(GHL_QUERY_ALL_PROJECTS)

    assert 'errors' not in result
    assert result['data']['allProjects']['count'] == 5


def test_success(ghl_auth_mock_info, all_projects_resolver):
    """Test success list project."""
    ProjectFactory.create_batch(5)
    resolved = all_projects_resolver(
        root=None,
        info=ghl_auth_mock_info,
    )

    assert resolved.length == 5


def test_unauth(ghl_mock_info, all_projects_resolver):
    """Test unauth list project access."""
    ProjectFactory.create_batch(5)

    with raises(PermissionDenied):
        all_projects_resolver(
            root=None,
            info=ghl_mock_info,
        )
