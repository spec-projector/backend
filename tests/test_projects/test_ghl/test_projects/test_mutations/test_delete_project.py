# -*- coding: utf-8 -*-

import pytest
from pytest import raises
from rest_framework.exceptions import PermissionDenied

from apps.projects.models import Project
from tests.test_projects.factories.project import ProjectFactory

GHL_QUERY_DELETE_PROJECT = """
mutation {{
    deleteProject(input: {{ project: "{pk}" }} ) {{
        errors {{
            field
        }}
        status
    }}
}}
"""


@pytest.fixture()
def project():
    return ProjectFactory.create()


def test_query(user, ghl_client, project):
    """Test delete project raw query."""
    ghl_client.set_user(user)

    result = ghl_client.execute(GHL_QUERY_DELETE_PROJECT.format(
        pk=project.pk,
    ))

    assert 'errors' not in result

    assert not Project.objects.exists()
    assert result['data']['deleteProject']['status'] == 'success'


def test_success(user, ghl_auth_mock_info, delete_project_mutation, project):
    """Test success delete."""
    result = delete_project_mutation(
        root=None,
        info=ghl_auth_mock_info,
        input={
            'project': project.pk,
        },
    )

    assert result.errors is None
    assert result.status == 'success'
    assert not Project.objects.exists()


def test_unauth(user, ghl_mock_info, delete_project_mutation, project):
    """Test unauthorized access."""
    with raises(PermissionDenied):
        delete_project_mutation(
            root=None,
            info=ghl_mock_info,
            input={
                'project': project.pk,
            },
        )


def test_not_found(user, ghl_auth_mock_info, delete_project_mutation, project):
    """Test project not found."""
    result = delete_project_mutation(
        root=None,
        info=ghl_auth_mock_info,
        input={
            'project': project.pk + 1,
        },
    )

    assert len(result.errors) == 1
    assert result.errors[0].field == 'project'
