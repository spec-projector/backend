from apps.media.models import Image
from apps.users.models import User


def test_delete_success(user1, image_instance):
    """Test delete success."""
    user_pk = user1.pk
    image_instance_pk = image_instance.pk

    user1.delete()

    assert not User.objects.filter(pk=user_pk).exists()
    assert not Image.objects.filter(pk=image_instance_pk).exists()
