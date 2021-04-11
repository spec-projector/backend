from typing import Any, Generic, TypeVar

from apps.core import injector

TCommand = TypeVar("TCommand")
TResult = TypeVar("TResult")


class CommandHandler(Generic[TCommand]):
    """Handler type hint."""

    def execute(self, command: TCommand) -> TResult:
        """Stub."""


class CommandBus:
    """Commands dispatcher."""

    def dispatch(self, command: Any) -> Any:  # type: ignore
        """Find command handler and executes it."""
        # CommandBus uses injector to find a handler
        command_handler = injector.get(
            CommandHandler[type(command)],  # type: ignore
        )
        return command_handler.execute(command)
