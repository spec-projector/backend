# -*- coding: utf-8 -*-

import pytest
from pytest import raises
from rest_framework.exceptions import PermissionDenied

from apps.projects.models import Project
from tests.test_projects.factories.project import ProjectFactory

GHL_QUERY_DELETE_PROJECT = """
mutation ($id: String!) {
    deleteProject(project: $id) {
        errors {
            field
        }
        status
    }
}
"""


@pytest.fixture()
def project():
    return ProjectFactory.create()


def test_query(user, ghl_client, project):
    """Test delete project raw query."""
    ghl_client.set_user(user)

    response = ghl_client.execute(
        GHL_QUERY_DELETE_PROJECT, variables={
            'id': project.pk,
        },
    )

    assert 'errors' not in response

    assert not Project.objects.exists()
    assert response['data']['deleteProject']['status'] == 'success'


def test_success(user, ghl_auth_mock_info, delete_project_mutation, project):
    """Test success delete."""
    response = delete_project_mutation(
        root=None,
        info=ghl_auth_mock_info,
        project=project.pk,
    )

    assert response.errors is None
    assert response.status == 'success'
    assert not Project.objects.exists()


def test_unauth(user, ghl_mock_info, delete_project_mutation, project):
    """Test unauthorized access."""
    with raises(PermissionDenied):
        delete_project_mutation(
            root=None,
            info=ghl_mock_info,
            project=project.pk,
        )


def test_not_found(user, ghl_auth_mock_info, delete_project_mutation, project):
    """Test project not found."""
    response = delete_project_mutation(
        root=None,
        info=ghl_auth_mock_info,
        project=project.pk + 1,
    )

    assert len(response.errors) == 1
    assert response.errors[0].field == 'project'
