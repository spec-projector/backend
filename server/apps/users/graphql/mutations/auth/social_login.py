from typing import Dict, Optional

import graphene
from graphql import ResolveInfo

from apps.core.graphql.mutations import BaseUseCaseMutation
from apps.users.logic.interfaces.social_login import SystemBackend
from apps.users.logic.use_cases.auth import social_login as social_login_uc


class SocialLoginMutation(BaseUseCaseMutation):
    """Login mutation through social."""

    class Meta:
        use_case_class = social_login_uc.UseCase

    class Arguments:
        system = graphene.Argument(
            graphene.Enum.from_enum(SystemBackend),
            required=True,
        )

    redirect_url = graphene.String()

    @classmethod
    def get_input_dto(
        cls,
        root: Optional[object],
        info: ResolveInfo,  # noqa: WPS110
        **kwargs,
    ):
        """Prepare use case input data."""
        return social_login_uc.InputDto(
            request=info.context,
            system=SystemBackend(kwargs["system"]),
        )

    @classmethod
    def get_response_data(
        cls,
        root: Optional[object],
        info: ResolveInfo,  # noqa: WPS110
        output_dto: social_login_uc.OutputDto,
    ) -> Dict[str, object]:
        """Prepare response data."""
        return {
            "redirect_url": output_dto.redirect_url,
        }
