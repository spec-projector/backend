from jnt_django_graphene_toolbox.errors import (
    GraphQLInputError,
    GraphQLPermissionDenied,
)

from apps.projects.models import Project

GHL_QUERY_CREATE_PROJECT = """
mutation ($title: String!, $description: String, $isPublic: Boolean) {
    createProject(title: $title, description: $description,
    isPublic: $isPublic) {
        project {
          id
          title
          isPublic
          description
        }
    }
}
"""


def test_query(user, ghl_client, couchdb_service):
    """Test create raw query."""
    ghl_client.set_user(user)

    response = ghl_client.execute(
        GHL_QUERY_CREATE_PROJECT,
        variable_values={"title": "my project"},
    )

    project = Project.objects.filter(title="my project").first()
    assert project is not None
    assert project.owner == user

    dto = response["data"]["createProject"]["project"]
    assert dto["id"] == str(project.id)
    assert dto["title"] == "my project"
    assert couchdb_service.create_database_called


def test_success(
    user,
    ghl_auth_mock_info,
    create_project_mutation,
    couchdb_service,
):
    """Test success create."""
    response = create_project_mutation(
        root=None,
        info=ghl_auth_mock_info,
        title="my project",
        is_public=True,
        description="description",
    )

    assert response.project is not None
    assert response.project.owner == user
    assert response.project.is_public
    assert response.project.description == "description"
    assert couchdb_service.create_database_called


def test_unauth(user, ghl_mock_info, create_project_mutation):
    """Test unauthorized access."""
    response = create_project_mutation(
        root=None,
        info=ghl_mock_info,
        title="my project",
    )

    assert isinstance(response, GraphQLPermissionDenied)


def test_empty_title(user, ghl_auth_mock_info, create_project_mutation):
    """Test bad input data."""
    response = create_project_mutation(
        root=None,
        info=ghl_auth_mock_info,
        title="",
    )

    assert isinstance(response, GraphQLInputError)
    assert not Project.objects.exists()
