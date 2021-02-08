import uuid

import pytest
from jnt_django_graphene_toolbox.errors import (
    GraphQLInputError,
    GraphQLPermissionDenied,
)
from jnt_django_graphene_toolbox.errors.input import INPUT_ERROR

from apps.projects.models import Project
from apps.projects.services.projects.couchdb import cleanup_couch_databases
from tests.test_projects.factories.project import ProjectFactory

GHL_QUERY_DELETE_PROJECT = """
mutation ($id: ID!) {
    deleteProject(project: $id) {
        status
    }
}
"""

PROJECT_DB_NAME = "db-1"


@pytest.fixture()
def project():
    """Provides project."""
    return ProjectFactory.create(db_name=PROJECT_DB_NAME)


def test_query(user, ghl_client, project):
    """Test delete project raw query."""
    ghl_client.set_user(user)

    response = ghl_client.execute(
        GHL_QUERY_DELETE_PROJECT,
        variable_values={"id": project.pk},
    )

    assert not Project.objects.exists()
    assert response["data"]["deleteProject"]["status"] == "success"


def test_success(
    user,
    ghl_auth_mock_info,
    delete_project_mutation,
    project,
):
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
    response = delete_project_mutation(
        root=None,
        info=ghl_mock_info,
        project=project.pk,
    )

    assert isinstance(response, GraphQLPermissionDenied)


def test_not_found(user, ghl_auth_mock_info, delete_project_mutation, project):
    """Test project not found."""
    response = delete_project_mutation(
        root=None,
        info=ghl_auth_mock_info,
        project=uuid.uuid4(),
    )

    assert isinstance(response, GraphQLInputError)
    assert response.extensions["code"] == INPUT_ERROR
    assert len(response.extensions["fieldErrors"]) == 1
    assert response.extensions["fieldErrors"][0]["fieldName"] == "project"


def test_delete_couch_db(
    user,
    ghl_auth_mock_info,
    delete_project_mutation,
    project,
    couchdb_service,
):
    """Test delete couch db."""
    response = delete_project_mutation(
        root=None,
        info=ghl_auth_mock_info,
        project=project.pk,
    )

    assert response.status == "success"
    assert not Project.objects.exists()

    cleanup_couch_databases()

    assert PROJECT_DB_NAME in couchdb_service.deleted_db_names
