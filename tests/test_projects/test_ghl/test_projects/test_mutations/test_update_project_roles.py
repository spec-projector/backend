# -*- coding: utf-8 -*-

import pytest
from django.db import models
from pytest import raises

from apps.core.graphql.errors import GraphQLInputError
from apps.projects.models import ProjectMember
from apps.projects.models.project_member import ProjectMemberRole
from tests.test_projects.factories.project import ProjectFactory
from tests.test_projects.factories.project_member import ProjectMemberFactory


@pytest.fixture()
def project():
    """Provides project."""
    return ProjectFactory.create()


def test_update_project_member_roles(
    user,
    project,
    update_project_mutation,
    ghl_auth_mock_info,
):
    """Test updating project member roles."""
    frontend = ProjectMember.roles.FRONTEND_DEVELOPER
    manager = ProjectMember.roles.PROJECT_MANAGER
    tester = ProjectMember.roles.TESTER

    query = models.Q(roles=frontend | manager)

    ProjectMemberFactory(
        user=user,
        project=project,
        roles=tester,
    )

    assert not ProjectMember.objects.filter(query).exists()

    users = [
        {
            "id": user.id,
            "roles": [
                ProjectMemberRole.FRONTEND_DEVELOPER,
                ProjectMemberRole.PROJECT_MANAGER,
            ],
        },
    ]

    update_project_mutation(
        root=None,
        info=ghl_auth_mock_info,
        id=project.pk,
        users=users,
    )

    assert ProjectMember.objects.filter(query).count() == 1
    assert not ProjectMember.objects.filter(roles=tester).exists()


def test_roles_not_setted_validate(
    user,
    project,
    update_project_mutation,
    ghl_auth_mock_info,
):
    """Test roles are not setted_validation."""
    users = [
        {
            "id": user.id,
        },
    ]

    with raises(GraphQLInputError):
        update_project_mutation(
            root=None,
            info=ghl_auth_mock_info,
            id=project.pk,
            users=users,
        )


def test_roles_is_empty(
    user,
    project,
    update_project_mutation,
    ghl_auth_mock_info,
):
    """Test roles are not empty validation."""
    users = [
        {
            "id": user.id,
            "roles": [],
        },
    ]

    with raises(GraphQLInputError):
        update_project_mutation(
            root=None,
            info=ghl_auth_mock_info,
            id=project.pk,
            users=users,
        )


def test_roles_not_valid(
    user,
    project,
    update_project_mutation,
    ghl_auth_mock_info,
):
    """Test roles are not valid validation."""
    users = [
        {
            "id": user.id,
            "roles": ["NO_VALID"],
        },
    ]

    with raises(GraphQLInputError):
        update_project_mutation(
            root=None,
            info=ghl_auth_mock_info,
            id=project.pk,
            users=users,
        )
