from typing import Dict, Optional, Union

from graphql import GraphQLError, ResolveInfo
from jnt_django_graphene_toolbox.errors import (
    GraphQLInputError,
    GraphQLPermissionDenied,
)
from jnt_django_graphene_toolbox.mutations import BaseMutation

from apps.core.graphql.errors import GenericGraphQLError
from apps.core.logic import commands
from apps.core.logic.errors import (
    AccessDeniedApplicationError,
    BaseApplicationError,
    InvalidInputApplicationError,
)


class BaseCommandMutation(BaseMutation):
    """Base class for mutations based on command."""

    class Meta:
        abstract = True

    @classmethod
    def mutate_and_get_payload(
        cls,
        root: Optional[object],
        info: ResolveInfo,  # noqa: WPS110
        **kwargs,
    ) -> Union["BaseCommandMutation", GraphQLError]:
        """Overrideable mutation operation."""
        try:
            command_result = commands.execute_command(
                cls.build_command(root, info, **kwargs),
            )
        except InvalidInputApplicationError as err:
            return GraphQLInputError(err.errors)
        except AccessDeniedApplicationError:
            return GraphQLPermissionDenied()
        except BaseApplicationError as err:
            return GenericGraphQLError(err)

        return cls(**cls.get_response_data(root, info, command_result))

    @classmethod
    def build_command(
        cls,
        root: Optional[object],
        info: ResolveInfo,  # noqa: WPS110
        validated_data,
    ):
        """Stub for getting command."""
        raise NotImplementedError()

    @classmethod
    def get_response_data(
        cls,
        root: Optional[object],
        info: ResolveInfo,  # noqa: WPS110
        command_result,
    ) -> Dict[str, object]:
        """Stub for getting usecase input dto."""
