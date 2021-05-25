from django.core.files.storage import default_storage

from apps.media.models import File, Image
from apps.projects.models import Project, ProjectAsset


def test_delete_success(project, project_asset, file_instance, image_instance):
    """Test delete success."""
    project_pk = project.pk
    project_asset_pk = project_asset.pk
    file_instance_pk = file_instance.pk
    image_instance_pk = image_instance.pk

    project.delete()

    assert not Project.objects.filter(pk=project_pk).exists()
    assert not ProjectAsset.objects.filter(pk=project_asset_pk).exists()
    assert not File.objects.filter(pk=file_instance_pk).exists()
    assert not Image.objects.filter(pk=image_instance_pk).exists()


def test_delete_as_queryset(project, project_asset, file_instance):
    """Test delete as queryset."""
    project_pk = project.pk
    project_asset_pk = project_asset.pk
    file_instance_pk = file_instance.pk

    Project.objects.filter(id=project_pk).delete()

    assert not Project.objects.filter(pk=project_pk).exists()
    assert not ProjectAsset.objects.filter(pk=project_asset_pk).exists()
    assert not File.objects.filter(pk=file_instance_pk).exists()


def test_delete_project_asset(project, project_asset, file_instance):
    """Test delete project asset."""
    project_pk = project.pk
    project_asset_pk = project_asset.pk
    file_instance_pk = file_instance.pk

    project_asset.delete()

    assert Project.objects.get(pk=project_pk)
    assert not ProjectAsset.objects.filter(pk=project_asset_pk).exists()
    assert not File.objects.filter(pk=file_instance_pk).exists()


def test_delete_file_instance(project, project_asset, file_instance):
    """Test delete file object."""
    project_pk = project.pk
    project_asset_pk = project_asset.pk
    file_instance_pk = file_instance.pk

    file_instance.delete()

    assert Project.objects.get(pk=project_pk)
    assert ProjectAsset.objects.get(pk=project_asset_pk)
    assert not File.objects.filter(pk=file_instance_pk).exists()


def test_delete_source_files(
    project,
    project_asset,
    file_instance,
    image_instance,
):
    """Test delete source files."""
    project_pk = project.pk
    file_source = file_instance.storage_file.name
    image_source = image_instance.storage_image.name

    project.delete()

    assert not Project.objects.filter(pk=project_pk).exists()
    assert not default_storage.exists(image_source)
    assert not default_storage.exists(file_source)
