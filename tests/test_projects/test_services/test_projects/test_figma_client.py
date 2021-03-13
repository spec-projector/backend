import pytest

from apps.projects.services.figma import FigmaService, InvalidUrlFigmaError
from tests.test_projects.factories.figma_integration import (
    FigmaIntegrationFactory,
)


@pytest.fixture()
def project(db):
    """:return project."""
    integration = FigmaIntegrationFactory.create()
    return integration.project


@pytest.fixture()
def figma_service(project):
    """:return FigmaService."""
    return FigmaService(project)


@pytest.mark.parametrize(
    ("figma_url", "f_key", "f_title", "f_id"),
    [
        (
            "https://www.figma.com/file/f1gma/file?node-id=123",
            "f1gma",
            "file",
            "123",
        ),
        (
            "https://www.figma.com/file/f1gma_key/file-name?node-id=3",
            "f1gma_key",
            "file-name",
            "3",
        ),
        (
            "https://www.figma.com/file/key/name?node-id=abc_s",
            "key",
            "name",
            "abc_s",
        ),
        (
            "https://www.figma.com/file/f1gma-key/file_name?node-id=a",
            "f1gma-key",
            "file_name",
            "a",
        ),
        (
            "https://www.figma.com/file/f1/fn?we=23&node-id=ids",
            "f1",
            "fn",
            "ids",
        ),
    ],
)
def test_valid_url_params(figma_service, figma_url, f_key, f_title, f_id):
    """Test parse image params."""
    image_params = figma_service.get_image_params(figma_url)

    assert image_params.key == f_key
    assert image_params.title == f_title
    assert image_params.id == f_id


@pytest.mark.parametrize(
    "figma_url",
    [
        "https://www.figma.com/file/f1gma_key/file-name?id=123",
        "https://www.figma.com/file/f1gma_key/file-name",
        "https://www.figma.com/file/f1gma_key?node-id=123",
        "https://www.figma.com/file/file-name?node-id=123",
        "https://www.figma.com/file?node-id=123",
    ],
)
def test_not_valid_params(figma_service, figma_url):
    """Test not valid url params."""
    with pytest.raises(InvalidUrlFigmaError):
        figma_service.get_image_params(figma_url)
