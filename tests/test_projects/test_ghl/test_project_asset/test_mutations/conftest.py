import pytest

from tests.test_projects.factories.figma_integration import (
    FigmaIntegrationFactory,
)
from tests.test_projects.factories.project import ProjectFactory


@pytest.fixture()
def project(db):
    """Create project."""
    project = ProjectFactory.create()
    FigmaIntegrationFactory.create(project=project)

    return project


@pytest.fixture(scope="session")
def upload_figma_asset_mutation(ghl_mutations):
    """Provides upload project asset graphql mutation."""
    return ghl_mutations.fields["uploadFigmaAsset"].resolver
