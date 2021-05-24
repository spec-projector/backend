import types
import typing

from django.apps import apps as django_apps
from django.core.files.storage import default_storage
from django.db import models

from apps.media.logic.interfaces import ICleanupMediaFilesService
from apps.media.models import File, Image

CLEANUP_MODELS_MAP = types.MappingProxyType(
    {
        Image: "storage_image",
        File: "storage_file",
    },
)


class CleanupMediaFilesService(ICleanupMediaFilesService):
    """Cleanup media files service."""

    def cleanup_media_files(self) -> None:
        """Cleanup media files."""
        for cleanup_model in CLEANUP_MODELS_MAP.keys():
            self._cleanup_model(cleanup_model)

    def _cleanup_model(self, current_model: models.Model) -> None:
        exclude_instances = []

        for model in self._get_models_with_relation(current_model):
            fields = self._get_related_fields(model, current_model)
            for field in fields:
                queryset = self._filter_queryset_by_field(
                    field,
                    model.objects.all(),
                )
                exclude_instances.extend(
                    queryset.values_list(field.name, flat=True),
                )

        self._delete_media_instances(
            current_model.objects.exclude(id__in=set(exclude_instances)),
        )

    def _delete_media_instances(self, queryset: models.QuerySet) -> None:
        field_name = CLEANUP_MODELS_MAP[queryset.model]
        for instance in queryset:
            media_field = getattr(instance, field_name)
            self._delete_media_from_storage(media_field)
            instance.delete()

    def _delete_media_from_storage(
        self,
        media_field: models.FileField,
    ) -> None:
        if default_storage.exists(media_field.name):
            default_storage.delete(media_field.name)

    def _filter_queryset_by_field(
        self,
        field: models.Field,
        queryset: models.QuerySet,
    ) -> models.QuerySet:
        if field.many_to_many:
            field_filter = ~models.Q(**{field.name: None})
        else:
            lookup = "{0}__isnull".format(field.name)
            field_filter = models.Q(**{lookup: False})

        return queryset.filter(field_filter)

    def _get_models_with_relation(
        self,
        relation_model: models.Model,
    ) -> typing.List[models.Model]:
        return [
            model
            for model in django_apps.get_models()
            if self._get_related_fields(model, relation_model)
        ]

    def _get_related_fields(
        self,
        model: models.Model,
        related_model: models.Model,
    ) -> typing.List[models.Field]:
        fields = model._meta.get_fields()  # noqa: WPS437
        return [
            field
            for field in fields
            if field.is_relation
            and not field.auto_created
            and field.related_model == related_model
        ]
