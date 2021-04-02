from typing import Dict, Optional

import graphene
from graphql import ResolveInfo

from apps.core.graphql.mutations import BaseUseCaseMutation
from apps.users.graphql.types import UserType
from apps.users.logic.use_cases.me import update as update_me_uc


class UpdateMeInput(graphene.InputObjectType):
    """User register input."""

    first_name = graphene.String()
    last_name = graphene.String()


class UpdateMeMutation(BaseUseCaseMutation):
    """Register mutation returns token."""

    class Meta:
        use_case_class = update_me_uc.UseCase
        auth_required = True

    class Arguments:
        input = graphene.Argument(UpdateMeInput, required=True)

    me = graphene.Field(UserType)

    @classmethod
    def get_input_dto(
        cls,
        root: Optional[object],
        info: ResolveInfo,  # noqa: WPS110
        **kwargs,
    ):
        """Prepare use case input data."""
        return update_me_uc.InputDto(
            user=info.context.user,  # type: ignore
            **kwargs["input"],
        )

    @classmethod
    def get_response_data(
        cls,
        root: Optional[object],
        info: ResolveInfo,  # noqa: WPS110
        output_dto: update_me_uc.OutputDto,
    ) -> Dict[str, object]:
        """Prepare response data."""
        return {"me": output_dto.user}
