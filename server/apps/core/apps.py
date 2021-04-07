from django.utils.translation import gettext_lazy as _
from jnt_django_toolbox.helpers.modules import load_module_from_app

from apps.core import injector
from apps.core.utils.apps import BaseAppConfig


class AppConfig(BaseAppConfig):
    """Base class for app config."""

    name = "apps.core"
    verbose_name = _("VN__CORE")

    def ready(self):
        """Trigger on app ready."""
        from apps.core.services.modules import (  # noqa: WPS433
            CoreInfrastructureModule,
        )

        super().ready()

        load_module_from_app(self, "models.lookups")
        injector.binder.install(CoreInfrastructureModule)
