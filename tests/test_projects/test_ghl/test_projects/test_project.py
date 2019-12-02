# -*- coding: utf-8 -*-

from pytest import raises
from rest_framework.exceptions import PermissionDenied

from apps.projects.graphql.types import ProjectType
from tests.test_projects.factories.project import ProjectFactory

GHL_QUERY_PROJECT = """
query {{
  project(id: {0}) {{
    id
    title
  }}
}}
"""


def test_query(user, ghl_client):
    """Test getting project query."""
    ghl_client.set_user(user)

    project = ProjectFactory.create()

    result = ghl_client.execute(GHL_QUERY_PROJECT.format(project.id))

    assert 'errors' not in result
    assert result['data']['project']['id'] == str(project.id)


def test_success(ghl_auth_mock_info):
    """Test success getting project."""
    project = ProjectFactory.create()

    retrieved = ProjectType().get_node(ghl_auth_mock_info, project.id)

    assert retrieved == project


def test_not_found(ghl_auth_mock_info):
    """Test project not found."""
    project = ProjectFactory.create()

    retrieved = ProjectType().get_node(ghl_auth_mock_info, project.id + 1)

    assert retrieved is None


def test_unauth(ghl_mock_info):
    """Test non authorized user."""
    project = ProjectFactory.create()

    with raises(PermissionDenied):
        ProjectType().get_node(ghl_mock_info, project.id)
