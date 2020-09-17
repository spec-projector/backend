# -*- coding: utf-8 -*-

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.users.models.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    """User model."""

    class Meta:
        verbose_name = _("VN__USER")
        verbose_name_plural = _("VN__USERS")
        ordering = ("login",)

    USERNAME_FIELD = "login"  # noqa: WPS115

    login = models.CharField(
        max_length=20,  # noqa:  WPS432
        blank=True,
        unique=True,
        verbose_name=_("VN__LOGIN"),
        help_text=_("HT__LOGIN"),
    )

    name = models.CharField(
        max_length=50,  # noqa:  WPS432
        blank=True,
        verbose_name=_("VN__NAME"),
        help_text=_("HT__NAME"),
    )

    email = models.EmailField(
        max_length=50,  # noqa:  WPS432
        blank=True,
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

    avatar = models.URLField(
        blank=True,
        verbose_name=_("VN__AVATAR"),
        help_text=_("HT__AVATAR"),
    )

    objects = UserManager()  # noqa: WPS110

    def __str__(self):
        """Text representation."""
        return self.login

    def get_short_name(self):
        """Get user short name."""
        return self.login
