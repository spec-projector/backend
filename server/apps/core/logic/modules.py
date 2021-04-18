import injector

from apps.core.logic.commands.handlers import CommandBus
from apps.core.logic.interfaces import ICommandBus


class CoreApplicationModule(injector.Module):
    """Setup di for core applications services."""

    def configure(self, binder: injector.Binder) -> None:
        """Bind services."""
        binder.bind(ICommandBus, CommandBus, scope=injector.singleton)
