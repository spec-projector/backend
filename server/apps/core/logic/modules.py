import injector

from apps.core.logic.commands.handlers import CommandBus


class CoreApplicationModule(injector.Module):
    """Setup di for core applications services."""

    def configure(self, binder: injector.Binder) -> None:
        """Bind services."""
        binder.bind(CommandBus, scope=injector.singleton)
