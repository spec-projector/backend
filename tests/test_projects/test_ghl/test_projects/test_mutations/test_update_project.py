# -*- coding: utf-8 -*-

import pytest
from pytest import raises
from rest_framework.exceptions import PermissionDenied

from tests.test_projects.factories.project import ProjectFactory

GHL_QUERY_UPDATE_PROJECT = """
mutation {{
    updateProject(input: {{ project: "{project}" {opts} }} ) {{
        errors {{
            field
        }}
        project {{
          id
          title
        }}
    }}
}}
"""


@pytest.fixture()
def project():
    return ProjectFactory.create()


def test_query(user, ghl_client, project):
    """Test update raw query."""
    ghl_client.set_user(user)

    result = ghl_client.execute(GHL_QUERY_UPDATE_PROJECT.format(
        project=project.pk,
        opts=', title: "new_{0}"'.format(project.title),
    ))

    assert 'errors' not in result

    dto = result['data']['updateProject']['project']
    assert dto['id'] == str(project.id)
    assert dto['title'] == 'new_{0}'.format(project.title)


def test_success(user, ghl_auth_mock_info, update_project_mutation, project):
    """Test success update."""
    result = update_project_mutation(
        root=None,
        info=ghl_auth_mock_info,
        input={
            'project': project.pk,
            'title': 'new title',
            'description': 'new description',
        },
    )

    assert result.project is not None
    assert result.project.title == 'new title'
    assert result.project.description == 'new description'


def test_unauth(user, ghl_mock_info, update_project_mutation, project):
    """Test unauthorized access."""
    with raises(PermissionDenied):
        update_project_mutation(
            root=None,
            info=ghl_mock_info,
            input={
                'project': project.pk,
                'title': 'new title',
                'description': 'new description',
            },
        )


def test_empty_data(user, ghl_auth_mock_info, update_project_mutation, project):
    """Test empty input data."""
    result = update_project_mutation(
        root=None,
        info=ghl_auth_mock_info,
        input={
            'project': project.pk,
            'title': '',
            'description': '',
        },
    )

    assert len(result.errors) == 2
