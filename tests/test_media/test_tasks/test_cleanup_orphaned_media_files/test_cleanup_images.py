from django.core.files.storage import default_storage

from apps.media.models import File, Image
from apps.media.tasks import cleanup_orphaned_media_files_task
from tests.test_media.factories.file import FileFactory
from tests.test_media.factories.image import ImageFactory
from tests.test_projects.factories import ProjectFactory


def test_no_cleanup(user):
    """Test no clenup."""
    user.avatar = ImageFactory.create()
    user.save()
    project = ProjectFactory.create(emblem=ImageFactory.create())
    cleanup_orphaned_media_files_task()

    user.refresh_from_db()
    project.refresh_from_db()
    assert user.avatar
    assert project.emblem


def test_cleanup_instances(user):
    """Test cleanup instances."""
    image_instance = ImageFactory.create().pk
    file_instance = FileFactory.create().pk
    user.avatar = ImageFactory.create()
    user.save()

    project1 = ProjectFactory.create(emblem=ImageFactory.create())
    project2 = ProjectFactory.create(emblem=user.avatar)

    cleanup_orphaned_media_files_task()

    user.refresh_from_db()
    project1.refresh_from_db()
    project2.refresh_from_db()

    assert user.avatar
    assert project1.emblem
    assert project2.emblem
    assert not Image.objects.filter(pk=image_instance).exists()
    assert not File.objects.filter(pk=file_instance).exists()


def test_cleanup_storage_image(user):
    """Test cleanup storage image."""
    image = ImageFactory.create().pk
    image_pk, image_file = image.pk, image.storage_image.name

    cleanup_orphaned_media_files_task()

    assert not Image.objects.filter(pk=image_pk).exists()
    assert not default_storage.exists(image_file)


def test_cleanup_storage_file(user):
    """Test cleanup storage file."""
    file_instance = FileFactory.create().pk
    file_pk, file_file = file_instance.pk, file_instance.storage_file.name

    cleanup_orphaned_media_files_task()

    assert not File.objects.filter(pk=file_pk).exists()
    assert not default_storage.exists(file_file)
