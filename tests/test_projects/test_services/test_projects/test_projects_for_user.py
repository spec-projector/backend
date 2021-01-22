import pytest

from apps.projects.models import Project
from apps.projects.services.projects.available_projects import (
    get_projects_for_user,
)
from tests.test_projects.factories.project import ProjectFactory
from tests.test_projects.factories.project_member import ProjectMemberFactory


@pytest.fixture(params=[True, False])
def project(db, request):
    """Create project."""
    return ProjectFactory.create(is_public=request.param)


@pytest.fixture()
def project_member(user, project):
    """Create project member."""
    return ProjectMemberFactory.create(user=user, project=project)


def test_not_projects(user, project):
    """Test empty projects."""
    projects = get_projects_for_user(Project.objects.all(), user)

    assert not projects.exists()


def test_projects_as_owner(user, project):
    """Test empty projects."""
    project.owner = user
    project.save()

    projects = get_projects_for_user(Project.objects.all(), user)

    assert projects.count() == 1
    assert projects.first() == project


def test_projects_as_project_member(user, project_member):
    """Test empty projects."""
    projects = get_projects_for_user(Project.objects.all(), user)

    assert projects.count() == 1
    assert projects.first() == project_member.project
