import hashlib

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.files.storage import default_storage
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.media.models.fields import ImageField
from apps.users.models.managers import UserManager


def avatar_upload_to(user, filename: str) -> str:
    """Generate folder for uploads."""
    user_hash = hashlib.md5(str(user.pk).encode()).hexdigest()  # noqa: S303
    return "users/{0}/{1}".format(user_hash, filename)


class User(AbstractBaseUser, PermissionsMixin):
    """User model."""

    class Meta:
        verbose_name = _("VN__USER")
        verbose_name_plural = _("VN__USERS")
        ordering = ("email",)

    USERNAME_FIELD = "email"  # noqa: WPS115

    first_name = models.CharField(
        max_length=50,  # noqa:  WPS432
        blank=True,
        verbose_name=_("VN__FIRST_NAME"),
        help_text=_("HT__FIRST_NAME"),
    )

    last_name = models.CharField(
        max_length=50,  # noqa:  WPS432
        blank=True,
        verbose_name=_("VN__LAST_NAME"),
        help_text=_("HT__LAST_NAME"),
    )

    email = models.EmailField(
        unique=True,
        db_index=True,
        verbose_name=_("VN__EMAIL"),
        help_text=_("HT__EMAIL"),
    )

    is_staff = models.BooleanField(
        default=True,
        verbose_name=_("VN__IS_STAFF"),
        help_text=_("HT__IS_STAFF"),
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name=_("VN__IS_ACTIVE"),
        help_text=_("HT__IS_ACTIVE"),
    )

    old_avatar = models.ImageField(
        upload_to=avatar_upload_to,
        max_length=256,  # noqa: WPS432
        blank=True,
        verbose_name=_("VN__AVATAR"),
        help_text=_("HT__AVATAR"),
    )
    avatar = ImageField(
        verbose_name=_("VN__AVATAR"),
        help_text=_("HT__AVATAR"),
    )

    objects = UserManager()  # noqa: WPS110

    def __str__(self):
        """Text representation."""
        return self.email

    def delete(self, *args, **kwargs):
        """Delete user."""
        image_path = self.avatar.path if self.avatar else None

        super().delete(*args, **kwargs)

        if image_path and default_storage.exists(image_path):
            default_storage.delete(image_path)

    def get_short_name(self):
        """Get user short name."""
        return self.first_name or self.email
