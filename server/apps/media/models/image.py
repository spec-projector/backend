from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models.mixins import Timestamps
from apps.core.utils.media import get_absolute_path
from apps.core.utils.objects import get_instance_hash


def get_upload_path(instance, filename) -> str:
    """Get upload path for instance."""
    if isinstance(instance, Image):
        return "images/{0}/{1}".format(get_instance_hash(instance), filename)
    return instance.get_upload_path(filename)


class Image(Timestamps):
    """Image."""

    class Meta:
        verbose_name = _("VN__IMAGE")
        verbose_name_plural = _("VN__IMAGES")

    storage_image = models.ImageField(
        upload_to=get_upload_path,
        max_length=1000,
        verbose_name=_("VN__STORAGE_IMAGE"),
        help_text=_("HT__STORAGE_IMAGE"),
    )
    original_filename = models.CharField(
        max_length=512,  # noqa: WPS432
        blank=True,
        verbose_name=_("VN__ORIGINAL_FILENAME"),
        help_text=_("HT__ORIGINAL_FILENAME"),
    )
    owner = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_("VN__OWNER"),
        help_text=_("HT__OWNER"),
    )

    def __str__(self):
        """Image present."""
        return self.original_filename

    def save(self, *args, **kwargs) -> None:
        """Save instance."""
        self._fill_original_filename()
        super().save(*args, **kwargs)

    @property
    def url(self):
        """Return absolute url."""
        return get_absolute_path(self.storage_image)

    def _fill_original_filename(self) -> None:
        """Fill original filename."""
        if self.original_filename:
            return

        self.original_filename = self.storage_image.name  # noqa: WPS601
