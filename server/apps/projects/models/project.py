# -*- coding: utf-8 -*-

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models.mixins import Timestamps


class Project(Timestamps):
    title = models.CharField(
        max_length=255,  # noqa: WPS432
        verbose_name=_('VN__TITLE'),
        help_text=_('HT__TITLE'),
    )

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        models.CASCADE,
        null=True,
        verbose_name=_('VN__OWNER'),
        help_text=_('HT__OWNER'),
    )

    class Meta:
        verbose_name = _('VN__PROJECT')
        verbose_name_plural = _('VN__PROJECTS')
        ordering = ('-created_at',)

    def __str__(self):
        return self.title
