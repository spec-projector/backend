import injector

from apps.core import services
from apps.core.logic import interfaces


class CoreInfrastructureModule(injector.Module):
    """Setup di for core services."""

    def configure(self, binder: injector.Binder) -> None:
        """Bind services."""
        binder.bind(interfaces.ICouchDBService, services.CouchDBService)
        binder.bind(
            interfaces.IEmailService,
            services.EmailService,
        )
        binder.bind(
            interfaces.IExternalFilesService,
            services.ExternalFilesService,
        )
        binder.bind(
            services.email.dispatcher.EmailDispatcher,
            scope=injector.singleton,
        )
