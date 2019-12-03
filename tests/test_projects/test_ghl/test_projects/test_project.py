# -*- coding: utf-8 -*-

from pytest import raises
from rest_framework.exceptions import PermissionDenied

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
    """Test getting project raw query."""
    ghl_client.set_user(user)

    project = ProjectFactory.create(owner=user)

    result = ghl_client.execute(GHL_QUERY_PROJECT.format(project.id))

    assert 'errors' not in result
    assert result['data']['project']['id'] == str(project.id)


def test_success(ghl_auth_mock_info, project_query):
    """Test success getting project."""
    project = ProjectFactory.create(owner=ghl_auth_mock_info.context.user)
    resolved = project_query(
        root=None,
        info=ghl_auth_mock_info,
        id=project.id,
    )

    assert resolved == project


def test_not_found(ghl_auth_mock_info, project_query):
    """Test project not found."""
    project = ProjectFactory.create()

    resolved = project_query(
        root=None,
        info=ghl_auth_mock_info,
        id=project.id + 1,
    )

    assert resolved is None


def test_unauth(ghl_mock_info, project_query):
    """Test non authorized user."""
    project = ProjectFactory.create()

    with raises(PermissionDenied):
        project_query(root=None, info=ghl_mock_info, id=project.id)
