import pytest

from apps.projects.models import ProjectAsset
from apps.projects.tasks import cleanup_project_assets_task
from tests.test_projects.factories.project_asset import ProjectAssetFactory


@pytest.fixture()
def project_asset(db):
    """Create project asset."""
    return ProjectAssetFactory.create()


def test_no_cleanup_project_assets_task(project_asset):
    """Test no cleanup with project."""
    assert project_asset.project

    cleanup_project_assets_task()
    project_asset.refresh_from_db()

    assert ProjectAsset.objects.filter(id=project_asset.pk).exists()


def test_cleanup_with_file(project_asset):
    """Test cleanup success."""
    project_asset.project = None
    project_asset.file = None
    project_asset.save()

    cleanup_project_assets_task()

    assert not ProjectAsset.objects.filter(id=project_asset.pk).exists()
