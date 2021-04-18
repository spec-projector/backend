import abc
from typing import Any, Generic, Type, TypeVar

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
