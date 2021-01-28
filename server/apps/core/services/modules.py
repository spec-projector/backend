import injector

from apps.core.services.couchdb import CouchDBService


class CoreServicesModule(injector.Module):
    """Setup di for user services."""

    def configure(self, binder: injector.Binder) -> None:
        """Bind services."""
        binder.bind(CouchDBService)
