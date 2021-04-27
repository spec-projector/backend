import abc
from typing import Any, Generic, Type, TypeVar

from apps.core import injector

TQuery = TypeVar("TQuery")
TResult = TypeVar("TResult")


class QueryHandler(Generic[TQuery]):
    """Handler type hint."""

    def execute(self, query: TQuery) -> TResult:
        """Stub."""


class IQueryBus(abc.ABC):
    """Commands dispatcher."""

    @abc.abstractmethod
    def register_handler(
        self,
        query_type: Type[TQuery],
        query_handler: Type[QueryHandler[TQuery]],
    ) -> None:
        """Register query handler."""

    @abc.abstractmethod
    def dispatch(self, query: Any) -> Any:  # type: ignore
        """Send query and get result."""


class QueryBus(IQueryBus):
    """Queries dispatcher."""

    def __init__(self):
        """Initializing."""
        self._registry = {}

    def register_handler(
        self,
        query_type: Type[TQuery],
        query_handler: Type[QueryHandler[TQuery]],
    ) -> None:
        """Register command handler."""
        self._registry[query_type] = query_handler

    def dispatch(self, query: Any) -> Any:  # type: ignore
        """Find command handler and executes it."""
        handler_type = self._registry.get(type(query))
        if not handler_type:
            raise ValueError(
                'Handler for query "{0}" is not registered'.format(
                    type(query),
                ),
            )
        query_handler = injector.get(handler_type)
        return query_handler.execute(query)
