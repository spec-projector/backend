from django.db import models
from django.dispatch import receiver

from apps.core.utils.media import cleanup_media_files


class BaseModel(models.Model):
    """Base model."""

    class Meta:
        abstract = True


@receiver(models.signals.post_delete)
def post_delete_base_model_handler(sender, instance, *args, **kwargs):
    """Base post delete handler."""
    if not isinstance(instance, BaseModel):
        return

    cleanup_media_files(instance)
