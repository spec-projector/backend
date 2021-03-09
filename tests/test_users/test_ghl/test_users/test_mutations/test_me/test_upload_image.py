from django.core.files.storage import default_storage
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image


def test_upload_image(
    user,
    ghl_auth_mock_info,
    upload_image_mutation,
    assets,
):
    """Test upload image."""
    image = assets.open_file("image.jpg")
    image_in_memory = InMemoryUploadedFile(
        image,
        "image",
        "middle.jpeg",
        "image/jpeg",
        42,
        "utf-8",
    )
    ghl_auth_mock_info.context.FILES[0] = image_in_memory

    assert not ghl_auth_mock_info.context.user.avatar.name

    width, height = 10, 15

    response = upload_image_mutation(
        root=None,
        info=ghl_auth_mock_info,
        input={
            "file": image_in_memory,
            "left": 0,
            "top": 0,
            "width": width,
            "height": height,
            "scale": 1,
        },
    )

    user.refresh_from_db()

    assert response.path
    assert default_storage.exists(user.avatar.path)
    assert response.path == user.avatar.url

    image = Image.open(default_storage.open(user.avatar.path))
    assert image.size == (width, height)
