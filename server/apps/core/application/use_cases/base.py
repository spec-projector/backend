import abc
import dataclasses
from typing import TypeVar

from apps.core.application.errors import InvalidInputApplicationError
from apps.core.utils.objects import Empty

TInputDto = TypeVar("TInputDto")
TOutputDto = TypeVar("TOutputDto")


def _non_empty_values_dict_factory(*args, **kwargs):
    new_args = (
        [
            (dict_key, dict_value)
            for dict_key, dict_value in args[0]
            if not isinstance(dict_value, Empty)
        ],
        *args[1:],
    )
    return dict(*new_args, **kwargs)


class BaseUseCase(abc.ABC):
    """Base class for use cases."""

    @abc.abstractmethod
    def execute(self, input_dto) -> None:
        """Main logic here."""

    def validate_input(self, input_data, validator_class):
        """
        Validate input data.

        Raise exception if data is invalid.
        """
        validator = validator_class(
            data=dataclasses.asdict(
                input_data,
                dict_factory=_non_empty_values_dict_factory,
            ),
        )
        if not validator.is_valid():
            raise InvalidInputApplicationError(validator.errors)

        return validator.validated_data
