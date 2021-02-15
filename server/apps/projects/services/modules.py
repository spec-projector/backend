import injector

from apps.projects.services.projects.figma import (
    FigmaServiceFactory,
    IFigmaServiceFactory,
)


class ProjectServicesModule(injector.Module):
    """Setup di for user services."""

    def configure(self, binder: injector.Binder) -> None:
        """Bind services."""
        binder.bind(IFigmaServiceFactory, FigmaServiceFactory)
