import injector

from apps.core.services.couchdb import CouchDBService, ICouchDBService
from apps.core.services.figma import FigmaServiceFactory, IFigmaServiceFactory


class CoreServicesModule(injector.Module):
    """Setup di for user services."""

    def configure(self, binder: injector.Binder) -> None:
        """Bind services."""
        binder.bind(ICouchDBService, CouchDBService)
        binder.bind(IFigmaServiceFactory, FigmaServiceFactory)
