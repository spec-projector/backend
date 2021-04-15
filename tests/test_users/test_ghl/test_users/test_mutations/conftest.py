import pytest
from django.core.files.uploadedfile import InMemoryUploadedFile

IMAGE_FILE = "image.jpg"


@pytest.fixture(scope="session")
def update_me_mutation(ghl_mutations):
    """
    Update me mutation.

    :param ghl_mutations:
    """
    return ghl_mutations.fields["updateMe"].resolver


@pytest.fixture()
def image_in_memory(assets):
    """Wrap image to in memory."""
    image = assets.open_file(IMAGE_FILE)
    return InMemoryUploadedFile(
        image,
        "image",
        "middle.jpeg",
        "image/jpeg",
        42,
        "utf-8",
    )


@pytest.fixture()
def image_in_memory2(assets):
    """Wrap image to in memory."""
    image = assets.open_file(IMAGE_FILE)
    return InMemoryUploadedFile(
        image,
        "image",
        "strong.jpeg",
        "image/jpeg",
        42,
        "utf-8",
    )
