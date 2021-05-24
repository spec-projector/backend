from jnt_django_graphene_toolbox.errors import (
    GraphQLInputError,
    GraphQLPermissionDenied,
)

from tests.test_media.factories.image import ImageFactory


def test_query(user, ghl_client, project, ghl_raw):
    """Test update raw query."""
    image = ImageFactory.create(owner=user)
    ghl_client.set_user(user)

    response = ghl_client.execute(
        ghl_raw("update_project"),
        variable_values={
            "id": project.pk,
            "input": {
                "title": "new_{0}".format(project.title),
                "emblem": image.pk,
            },
        },
    )

    dto = response["data"]["updateProject"]["project"]
    assert dto["id"] == str(project.id)
    assert dto["title"] == "new_{0}".format(project.title)
    assert dto["emblem"]["id"] == str(image.pk)


def test_success(user, ghl_auth_mock_info, update_project_mutation, project):
    """Test success update."""
    response = update_project_mutation(
        root=None,
        info=ghl_auth_mock_info,
        id=project.pk,
        input={
            "title": "new title",
            "description": "new description",
        },
    )

    assert response.project is not None
    assert response.project.title == "new title"
    assert response.project.description == "new description"


def test_unauth(user, ghl_mock_info, update_project_mutation, project):
    """Test unauthorized access."""
    response = update_project_mutation(
        root=None,
        info=ghl_mock_info,
        id=project.pk,
        input={
            "title": "new title",
            "description": "new description",
        },
    )

    assert isinstance(response, GraphQLPermissionDenied)


def test_empty_data(
    user,
    ghl_auth_mock_info,
    update_project_mutation,
    project,
):
    """Test empty input data."""
    response = update_project_mutation(
        root=None,
        info=ghl_auth_mock_info,
        id=project.pk,
        input={
            "title": "",
            "description": "",
        },
    )

    assert isinstance(response, GraphQLInputError)
    assert len(response.extensions["fieldErrors"]) == 2


def test_change_is_public(
    user,
    project,
    update_project_mutation,
    ghl_auth_mock_info,
):
    """Test update project is public."""
    project.is_public = False
    project.save()

    response = update_project_mutation(
        root=None,
        info=ghl_auth_mock_info,
        id=project.pk,
        input={
            "is_public": True,
        },
    )

    assert response.project is not None
    assert response.project.is_public


def test_update_emblem(
    user,
    project,
    update_project_mutation,
    ghl_auth_mock_info,
):
    """Test update emblem."""
    image = ImageFactory.create(owner=user)
    response = update_project_mutation(
        root=None,
        info=ghl_auth_mock_info,
        id=project.pk,
        input={
            "is_public": True,
            "emblem": image.pk,
        },
    )

    assert response.project is not None
    assert response.project.emblem == image
