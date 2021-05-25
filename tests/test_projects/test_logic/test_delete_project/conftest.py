import pytest

from tests.test_media.factories.file import FileFactory
from tests.test_media.factories.image import ImageFactory
from tests.test_projects.factories import ProjectAssetFactory, ProjectFactory


@pytest.fixture()
def project(image_instance):
    """Create project."""
    return ProjectFactory.create(emblem=image_instance)


@pytest.fixture()
def file_instance(db):
    """Create file instance."""
    return FileFactory.create()


@pytest.fixture()
def image_instance(db):
    """Create image."""
    return ImageFactory.create()


@pytest.fixture()
def project_asset(project, file_instance):
    """Create project asset."""
    return ProjectAssetFactory.create(project=project, file=file_instance)
