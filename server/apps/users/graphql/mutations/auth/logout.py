from typing import Dict, Optional

import graphene
from graphql import ResolveInfo

from apps.core.graphql.mutations import BaseUseCaseMutation
from apps.users.logic.use_cases.auth import logout as logout_uc


class LogoutMutation(BaseUseCaseMutation):
    """Logout mutation."""

    class Meta:
        auth_required = True
        use_case_class = logout_uc.UseCase

    status = graphene.String()

    @classmethod
    def get_input_dto(
        cls,
        root: Optional[object],
        info: ResolveInfo,  # noqa: WPS110
        **kwargs,
    ):
        """Prepare use case input data."""
        return logout_uc.InputDto(
            token=info.context.auth,
        )

    @classmethod
    def get_response_data(
        cls,
        root: Optional[object],
        info: ResolveInfo,  # noqa: WPS110
        output_dto,
    ) -> Dict[str, object]:
        """Prepare response data."""
        return {
            "status": "success",
        }
