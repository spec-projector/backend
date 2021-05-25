import pytest

from tests.test_media.factories.image import ImageFactory
from tests.test_users.factories.user import UserFactory


@pytest.fixture()
def image_instance(db):
    """Create image."""
    return ImageFactory.create()


@pytest.fixture()
def user1(image_instance):
    """Create user."""
    return UserFactory.create(avatar=image_instance)
