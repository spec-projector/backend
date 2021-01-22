import pytest
from django.contrib.auth.models import AnonymousUser

from apps.projects.models import Project
from apps.projects.services.projects.available_projects import (
    get_available_projects,
)
from tests.test_projects.factories.project import ProjectFactory
from tests.test_projects.factories.project_member import ProjectMemberFactory


@pytest.fixture()
def project(db):
    """Create project."""
    return ProjectFactory.create(is_public=True)


@pytest.fixture()
def unpublic_project(db):
    """Create project."""
    return ProjectFactory.create(is_public=False)


@pytest.fixture()
def project_member(user, project):
    """Create project member."""
    return ProjectMemberFactory.create(user=user, project=project)


def test_as_anonymus(project, unpublic_project):
    """Test available is public project."""
    projects = get_available_projects(Project.objects.all(), AnonymousUser)

    assert projects.count() == 1
    assert projects.first() == project


def test_projects_as_owner(user, project, unpublic_project):
    """Test empty projects."""
    project.owner = user
    project.save()

    projects = get_available_projects(Project.objects.all(), user)

    assert projects.count() == 1
    assert projects.first() == project


def test_projects_as_project_member(user, project_member, unpublic_project):
    """Test empty projects."""
    projects = get_available_projects(Project.objects.all(), user)

    assert projects.count() == 1
    assert projects.first() == project_member.project
