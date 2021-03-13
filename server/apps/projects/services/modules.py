import injector

from apps.projects.services.figma import (
    FigmaServiceFactory,
    IFigmaServiceFactory,
)


class ProjectInfrastructureServicesModule(injector.Module):
    """Setup di for user services."""

    def configure(self, binder: injector.Binder) -> None:
        """Bind services."""
        binder.bind(IFigmaServiceFactory, FigmaServiceFactory)
