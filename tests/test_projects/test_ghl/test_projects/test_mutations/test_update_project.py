# -*- coding: utf-8 -*-

import pytest
from pytest import raises

from apps.core.graphql.errors import GraphQLInputError, GraphQLPermissionDenied
from tests.test_projects.factories.project import ProjectFactory

GHL_QUERY_UPDATE_PROJECT = """
mutation ($id: String!, $title: String) {
    updateProject(project: $id, title: $title) {
        project {
          id
          title
        }
    }
}
"""


@pytest.fixture()
def project():
    return ProjectFactory.create()


def test_query(user, ghl_client, project):
    """Test update raw query."""
    ghl_client.set_user(user)

    response = ghl_client.execute(
        GHL_QUERY_UPDATE_PROJECT,
        variables={
            "id": project.pk,
            "title": "new_{0}".format(project.title),
        },
    )

    dto = response["data"]["updateProject"]["project"]
    assert dto["id"] == str(project.id)
    assert dto["title"] == "new_{0}".format(project.title)


def test_success(user, ghl_auth_mock_info, update_project_mutation, project):
    """Test success update."""
    response = update_project_mutation(
        root=None,
        info=ghl_auth_mock_info,
        project=project.pk,
        title="new title",
        description="new description",
    )

    assert response.project is not None
    assert response.project.title == "new title"
    assert response.project.description == "new description"


def test_unauth(user, ghl_mock_info, update_project_mutation, project):
    """Test unauthorized access."""
    with raises(GraphQLPermissionDenied):
        update_project_mutation(
            root=None,
            info=ghl_mock_info,
            project=project.pk,
            title="new title",
            description="new description",
        )


def test_empty_data(user, ghl_auth_mock_info, update_project_mutation, project):
    """Test empty input data."""
    with raises(GraphQLInputError) as exc_info:
        update_project_mutation(
            root=None,
            info=ghl_auth_mock_info,
            project=project.pk,
            title="",
            description="",
        )

    extensions = exc_info.value.extensions  # noqa:WPS441

    assert len(extensions["fieldErrors"]) == 2
