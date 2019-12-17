# -*- coding: utf-8 -*-

from pytest import raises
from rest_framework.exceptions import PermissionDenied

from apps.projects.models import Project

GHL_QUERY_CREATE_PROJECT = """
mutation ($title: String!) {
    createProject(title: $title) {
        errors {
            field
        }
        project {
          id
          title
        }
    }
}
"""


def test_query(user, ghl_client):
    """Test create raw query."""
    ghl_client.set_user(user)

    response = ghl_client.execute(
        GHL_QUERY_CREATE_PROJECT,
        variables={
            'title': 'my project',
        },
    )

    assert 'errors' not in response

    project = Project.objects.filter(title='my project').first()
    assert project is not None
    assert project.owner == user

    dto = response['data']['createProject']['project']
    assert dto['id'] == str(project.id)
    assert dto['title'] == 'my project'


def test_success(user, ghl_auth_mock_info, create_project_mutation):
    """Test success create."""
    response = create_project_mutation(
        root=None,
        info=ghl_auth_mock_info,
        title='my project',
    )

    assert response.project is not None
    assert response.project.owner == user


def test_unauth(user, ghl_mock_info, create_project_mutation):
    """Test unauthorized access."""
    with raises(PermissionDenied):
        create_project_mutation(
            root=None,
            info=ghl_mock_info,
            title='my project',
        )


def test_empty_title(user, ghl_auth_mock_info, create_project_mutation):
    """Test bad input data."""
    response = create_project_mutation(
        root=None,
        info=ghl_auth_mock_info,
        title='',
    )

    assert response.errors is not None
    assert not Project.objects.exists()
