import abc
from typing import Any, Generic, Type, TypeVar

from apps.core import injector

TCommand = TypeVar("TCommand")
TResult = TypeVar("TResult")


class CommandHandler(Generic[TCommand]):
    """Handler type hint."""

    def execute(self, command: TCommand) -> TResult:
        """Stub."""


class ICommandBus(abc.ABC):
    """Commands dispatcher."""

    @abc.abstractmethod
    def register_handler(
        self,
        command_type: Type[TCommand],
        command_handler: Type[CommandHandler[TCommand]],
    ) -> None:
        """Register command handler."""

    @abc.abstractmethod
    def dispatch(self, command: Any) -> Any:  # type: ignore
        """Send command and get result."""


class CommandBus(ICommandBus):
    """Commands dispatcher."""

    def __init__(self):
        """Initializing."""
        self._registry = {}

    def register_handler(
        self,
        command_type: Type[TCommand],
        command_handler: Type[CommandHandler[TCommand]],
    ) -> None:
        """Register command handler."""
        self._registry[command_type] = command_handler

    def dispatch(self, command: Any) -> Any:  # type: ignore
        """Find command handler and executes it."""
        handler_type = self._registry.get(type(command))
        if not handler_type:
            raise ValueError(
                'Handler for command "{0}" is not registered'.format(
                    type(command),
                ),
            )
        command_handler = injector.get(handler_type)
        return command_handler.execute(command)
