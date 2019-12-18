# -*- coding: utf-8 -*-

from typing import Iterable, Optional

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models.mixins import Timestamps
from apps.core.utils.hash import generate_md5


class Project(Timestamps):
    title = models.CharField(
        max_length=255,  # noqa: WPS432
        verbose_name=_('VN__TITLE'),
        help_text=_('HT__TITLE'),
    )

    description = models.TextField(
        verbose_name=_('VN__DESCRIPTION'),
        help_text=_('HT__DESCRIPTION'),
    )

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        models.CASCADE,
        null=True,
        verbose_name=_('VN__OWNER'),
        help_text=_('HT__OWNER'),
    )

    uid = models.CharField(
        max_length=32,  # noqa: WPS432
        verbose_name=_('VN__UID'),
        help_text=_('HT__UID'),
        default='',
    )

    class Meta:
        verbose_name = _('VN__PROJECT')
        verbose_name_plural = _('VN__PROJECTS')
        ordering = ('-created_at',)

    def __str__(self):
        return self.title

    def save(
        self,
        force_insert: bool = False,
        force_update: bool = False,
        using: Optional[str] = None,
        update_fields: Optional[Iterable[str]] = None,
    ) -> None:
        if not self.uid:
            self.uid = generate_md5()  # noqa: WPS601

        super().save(
            force_insert=force_insert,
            force_update=force_update,
            using=using,
            update_fields=update_fields,
        )
