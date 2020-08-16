# -*- coding: utf-8 -*-

import pytest
from jnt_django_graphene_toolbox.errors import GraphQLPermissionDenied

from tests.test_projects.factories.project import ProjectFactory
from tests.test_projects.factories.project_member import ProjectMemberFactory

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
    response = all_projects_query(root=None, info=ghl_auth_mock_info)

    assert response.length == 5


def test_unauth(ghl_mock_info, all_projects_query):
    """Test unauth list project access."""
    ProjectFactory.create_batch(2, public=True)
    ProjectFactory.create_batch(2, public=False)

    with pytest.raises(GraphQLPermissionDenied):
        all_projects_query(
            root=None, info=ghl_mock_info,
        )


def test_all_projects_not_owner(ghl_auth_mock_info, all_projects_query):
    """Test get project if not owner."""
    projects = ProjectFactory.create_batch(5)
    project = projects[0]

    ProjectMemberFactory.create(
        project=project, user=ghl_auth_mock_info.context.user,
    )

    response = all_projects_query(root=None, info=ghl_auth_mock_info)

    assert response.length == 1
    assert response.edges[0].node == project
