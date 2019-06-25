from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.db.mixins import Timestamps


class Project(Timestamps):
    title = models.CharField(
        max_length=255,
        verbose_name=_('VN__TITLE'),
        help_text=_('HT__TITLE')
    )

    class Meta:
        verbose_name = _('VN__PROJECT')
        verbose_name_plural = _('VN__PROJECTS')
        ordering = ('-created_at',)

    def __str__(self):
        return self.title