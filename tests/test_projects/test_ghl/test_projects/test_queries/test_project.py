from tests.test_projects.factories.project import ProjectFactory

GHL_QUERY_PROJECT = """
query ($id: ID!) {
  project(id: $id) {
    id
    title
  }
}
"""


def test_query(user, ghl_client):
    """Test getting project raw query."""
    ghl_client.set_user(user)

    project = ProjectFactory.create(owner=user)

    response = ghl_client.execute(
        GHL_QUERY_PROJECT,
        variable_values={"id": project.id},
    )

    assert "errors" not in response
    assert response["data"]["project"]["id"] == str(project.id)


def test_success(ghl_auth_mock_info, project_query):
    """Test success getting project."""
    project = ProjectFactory.create(owner=ghl_auth_mock_info.context.user)
    response = project_query(
        root=None,
        info=ghl_auth_mock_info,
        id=project.id,
    )

    assert response == project


def test_not_found(ghl_auth_mock_info, project_query):
    """Test project not found."""
    ProjectFactory.create()

    response = project_query(
        root=None,
        info=ghl_auth_mock_info,
        id="1",
    )
    assert response is None


def test_unauth(ghl_mock_info, project_query, db):
    """Test non authorized user."""
    project = ProjectFactory.create(is_public=False)

    response = project_query(root=None, info=ghl_mock_info, id=project.id)

    assert response is None


def test_retrieve_public_project(ghl_mock_info, project_query, db):
    """Test getting public project not authorized user."""
    project = ProjectFactory.create(is_public=True)

    response = project_query(root=None, info=ghl_mock_info, id=project.id)

    assert response == project


def test_retrieve_unpublic_project(ghl_mock_info, project_query, db):
    """Test getting not public project not authorized user."""
    ProjectFactory.create(is_public=True)
    project = ProjectFactory.create(is_public=False)

    response = project_query(root=None, info=ghl_mock_info, id=project.id)

    assert response is None
