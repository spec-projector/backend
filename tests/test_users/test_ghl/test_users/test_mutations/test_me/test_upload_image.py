from django.core.files.storage import default_storage
from PIL import Image


def test_upload_me_avatar(
    user,
    ghl_auth_mock_info,
    upload_me_avatar_mutation,
    image_in_memory,
):
    """Test upload image."""
    ghl_auth_mock_info.context.FILES[0] = image_in_memory

    assert not ghl_auth_mock_info.context.user.avatar.name

    width, height = 10, 15

    response = upload_me_avatar_mutation(
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

    assert response.user
    assert response.user == user

    image = Image.open(default_storage.open(user.avatar.path))
    assert image.size == (width, height)


def test_upload_if_exists_avatar(
    user,
    ghl_auth_mock_info,
    upload_me_avatar_mutation,
    image_in_memory,
    image_in_memory2,
):
    """Test upload if user avatar exists."""
    user.avatar = image_in_memory
    user.save()

    avatar_path = user.avatar.path

    ghl_auth_mock_info.context.FILES[0] = image_in_memory2

    response = upload_me_avatar_mutation(
        root=None,
        info=ghl_auth_mock_info,
        input={
            "file": image_in_memory,
            "left": 0,
            "top": 0,
            "width": 10,
            "height": 15,
            "scale": 1,
        },
    )

    user.refresh_from_db()

    assert response.user == user
    assert user.avatar.path != avatar_path
    assert not default_storage.exists(avatar_path)
