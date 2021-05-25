import typing

from django.conf import settings
from django.core.files.storage import default_storage
from django.db import models


def get_absolute_path(file_field: models.FileField) -> str:
    """Generate absolute file path."""
    if file_field:
        return "https://{0}{1}{2}".format(
            settings.DOMAIN_NAME,
            settings.MEDIA_URL,
            file_field.name,
        )

    return file_field


def cleanup_media_files(instance):
    """Cleanup media files."""
    from apps.media.models import File, Image  # noqa: WPS433

    for file_field in _get_media_fields(instance, File):
        media_instance = getattr(instance, file_field.name)
        if media_instance:
            _delete_file(media_instance)

    for image_field in _get_media_fields(instance, Image):
        media_instance = getattr(instance, image_field.name)
        if media_instance:
            _delete_image(media_instance)


def _delete_file(file_instance) -> None:
    _delete_media_from_storage(file_instance.storage_file)
    file_instance.delete()


def _delete_image(image_instance) -> None:
    _delete_media_from_storage(image_instance.storage_image)
    image_instance.delete()


def _delete_media_from_storage(media_field: models.FileField) -> None:
    if media_field and default_storage.exists(media_field.name):
        default_storage.delete(media_field.name)


def _get_media_fields(instance, related_model) -> typing.List[models.Field]:
    return [
        field
        for field in instance._meta.get_fields()  # noqa: WPS437
        if field.is_relation
        and not field.auto_created
        and field.related_model == related_model
    ]
