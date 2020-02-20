# -*- coding: utf-8 -*-

import uuid

import pytest
from pytest import raises

from apps.core.graphql.errors import (
    INPUT_ERROR,
    GraphQLInputError,
    GraphQLPermissionDenied,
)
from apps.projects.models import Project
from tests.test_projects.factories.project import ProjectFactory

GHL_QUERY_DELETE_PROJECT = """
mutation ($id: ID!) {
    deleteProject(project: $id) {
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
            "id": project.pk,
        },
    )

    assert not Project.objects.exists()
    assert response["data"]["deleteProject"]["status"] == "success"


def test_success(user, ghl_auth_mock_info, delete_project_mutation, project):
    """Test success delete."""
    response = delete_project_mutation(
        root=None,
        info=ghl_auth_mock_info,
        project=project.pk,
    )

    assert response.status == "success"
    assert not Project.objects.exists()


def test_unauth(user, ghl_mock_info, delete_project_mutation, project):
    """Test unauthorized access."""
    with raises(GraphQLPermissionDenied):
        delete_project_mutation(
            root=None,
            info=ghl_mock_info,
            project=project.pk,
        )


def test_not_found(user, ghl_auth_mock_info, delete_project_mutation, project):
    """Test project not found."""
    with raises(GraphQLInputError) as exc_info:
        delete_project_mutation(
            root=None,
            info=ghl_auth_mock_info,
            project=uuid.uuid4(),
        )

    extensions = exc_info.value.extensions  # noqa:WPS441
    assert extensions["code"] == INPUT_ERROR

    assert len(extensions["fieldErrors"]) == 1
    assert extensions["fieldErrors"][0]["fieldName"] == "project"
