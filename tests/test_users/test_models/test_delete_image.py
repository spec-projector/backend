import pytest
from django.core.files.storage import default_storage
from django.core.files.uploadedfile import SimpleUploadedFile

from tests.test_users.factories.user import UserFactory


@pytest.fixture()
def image(assets) -> SimpleUploadedFile:
    """Open image as simple uploaded file."""
    return SimpleUploadedFile(
        name="image.jpg",
        content=assets.open_file("image.jpg").read(),
        content_type="image/jpeg",
    )


def test_delete_image(db, image):
    """Test delete image on user delete."""
    user = UserFactory.create(avatar=image)
    image_path = user.avatar.path

    assert default_storage.exists(image_path)

    user.delete()

    assert not default_storage.exists(image_path)


def test_delete_without_mage(db):
    """Test delete without image."""
    user = UserFactory.create(avatar="")
    user.delete()
