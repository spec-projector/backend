from typing import Dict, Optional

import graphene
from graphql import ResolveInfo

from apps.core.graphql.mutations import BaseUseCaseMutation
from apps.users.logic.use_cases.change_password import (
    change_password as change_password_uc,
)


class ChangePasswordInput(graphene.InputObjectType):
    """Input change password."""

    password = graphene.String(required=True)


class ChangePasswordMutation(BaseUseCaseMutation):
    """Change password mutation."""

    class Meta:
        use_case_class = change_password_uc.UseCase
        auth_required = True

    class Arguments:
        input = graphene.Argument(ChangePasswordInput, required=True)

    ok = graphene.Boolean()

    @classmethod
    def get_input_dto(
        cls,
        root: Optional[object],
        info: ResolveInfo,  # noqa: WPS110
        **kwargs,
    ):
        """Prepare use case input data."""
        user = info.context.user  # type: ignore
        return change_password_uc.InputDto(
            password=kwargs["input"]["password"],
            user=user,
        )

    @classmethod
    def get_response_data(
        cls,
        root: Optional[object],
        info: ResolveInfo,  # noqa: WPS110
        output_dto: change_password_uc.OutputDto,
    ) -> Dict[str, object]:
        """Prepare response data."""
        return {"ok": output_dto.ok}
