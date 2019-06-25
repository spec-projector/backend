from django.utils.translation import gettext_lazy as _

from apps.core.apps import BaseAppConfig


class AppConfig(BaseAppConfig):
    name = 'apps.projects'
    verbose_name = _('VN__PROJECTS')
