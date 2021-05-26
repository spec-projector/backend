from django.db import models
from jnt_django_graphene_toolbox.errors import GraphQLInputError

from apps.projects.models import ProjectMember
from apps.projects.models.enums import ProjectPermission
from apps.projects.models.project_member import ProjectMemberRole
from tests.test_projects.factories.project_member import ProjectMemberFactory


def test_update_project_member_permissions(
    user,
    project,
    update_project_mutation,
    ghl_auth_mock_info,
):
    """Test updating project member roles."""
    feature_api = ProjectMember.permissions.EDIT_FEATURE_API
    sprints = ProjectMember.permissions.EDIT_SPRINTS
    terms = ProjectMember.permissions.EDIT_TERMS

    query = models.Q(permissions=feature_api | sprints)

    ProjectMemberFactory(
        user=user,
        project=project,
        permissions=terms,
    )

    assert not ProjectMember.objects.filter(query).exists()

    users = [
        {
            "id": user.id,
            "permissions": [
                ProjectPermission.EDIT_FEATURE_API,
                ProjectPermission.EDIT_SPRINTS,
            ],
            "role": ProjectMemberRole.EDITOR,
        },
    ]

    update_project_mutation(
        root=None,
        info=ghl_auth_mock_info,
        id=project.pk,
        input={
            "members": users,
        },
    )

    assert ProjectMember.objects.filter(query).count() == 1
    assert not ProjectMember.objects.filter(permissions=terms).exists()


def test_roles_not_setted_validate(
    user,
    project,
    update_project_mutation,
    ghl_auth_mock_info,
):
    """Test roles are not setted_validation."""
    users = [
        {"id": user.id},
    ]

    response = update_project_mutation(
        root=None,
        info=ghl_auth_mock_info,
        id=project.pk,
        input={
            "members": users,
        },
    )
    assert isinstance(response, GraphQLInputError)


def test_roles_is_empty(
    user,
    project,
    update_project_mutation,
    ghl_auth_mock_info,
):
    """Test roles are not empty validation."""
    users = [
        {"id": user.id, "roles": []},
    ]

    response = update_project_mutation(
        root=None,
        info=ghl_auth_mock_info,
        id=project.pk,
        input={
            "members": users,
        },
    )

    assert isinstance(response, GraphQLInputError)


def test_roles_not_valid(
    user,
    project,
    update_project_mutation,
    ghl_auth_mock_info,
):
    """Test roles are not valid validation."""
    users = [
        {"id": user.id, "roles": ["NO_VALID"]},
    ]

    response = update_project_mutation(
        root=None,
        info=ghl_auth_mock_info,
        id=project.pk,
        input={
            "members": users,
        },
    )

    assert isinstance(response, GraphQLInputError)
