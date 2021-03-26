import pytest
from django.contrib.auth.models import AnonymousUser
from django.db import models

from apps.projects.logic.queries.project import allowed
from tests.test_projects.factories.project import ProjectFactory
from tests.test_projects.factories.project_member import ProjectMemberFactory


@pytest.fixture()
def public_project(db):
    """Create project."""
    return ProjectFactory.create(is_public=True)


@pytest.fixture()
def private_project(db):
    """Create project."""
    return ProjectFactory.create(is_public=False)


def test_as_anonymus(public_project, private_project):
    """Test available is public project."""
    projects = _execute_query(AnonymousUser)

    assert projects.count() == 1
    assert projects.first() == public_project


def test_projects_as_owner(user, private_project):
    """Test empty projects."""
    private_project.owner = user
    private_project.save()

    projects = _execute_query(user)

    assert projects.count() == 1
    assert projects.first() == private_project


def test_user_is_project_member(user, project_member, private_project):
    """Test empty projects."""
    ProjectMemberFactory.create(user=user, project=private_project)

    projects = _execute_query(user)

    assert projects.count() == 1
    assert projects.first() == project_member.project


def test_user_and_public_project(user, public_project, private_project):
    """Test empty projects."""
    projects = _execute_query(user)

    assert projects.count() == 1
    assert projects.first() == public_project


def _execute_query(user) -> models.QuerySet:
    return allowed.Query().execute(
        allowed.InputDto(
            user=user,
            include_public=True,
        ),
    )
