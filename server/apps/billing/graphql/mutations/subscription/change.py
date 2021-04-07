from typing import Dict, Optional

import graphene
from graphql import ResolveInfo

from apps.billing.graphql.types.change_subscription_request import (
    ChangeSubscriptionRequestType,
)
from apps.billing.logic.use_cases.subscription import (
    change as change_subscription,
)
from apps.core.graphql.mutations import BaseUseCaseMutation


class ChangeSubscriptionInput(graphene.InputObjectType):
    """Input for create project asset."""

    tariff = graphene.ID(required=True)
    hash = graphene.String(required=True)


class ChangeSubscriptionMutation(BaseUseCaseMutation):
    """Change subscription mutation."""

    class Meta:
        use_case_class = change_subscription.UseCase
        auth_required = True

    class Arguments:
        input = graphene.Argument(  # noqa: WPS125
            ChangeSubscriptionInput,
            required=True,
        )

    request = graphene.Field(ChangeSubscriptionRequestType)

    @classmethod
    def get_input_dto(
        cls,
        root: Optional[object],
        info: ResolveInfo,  # noqa: WPS110
        **kwargs,
    ):
        """Prepare use case input data."""
        return change_subscription.InputDto(
            user=info.context.user,  # type: ignore
            tariff=kwargs["tariff"],
            hash=kwargs["hash"],
        )

    @classmethod
    def get_response_data(
        cls,
        root: Optional[object],
        info: ResolveInfo,  # noqa: WPS110
        output_dto: change_subscription.OutputDto,
    ) -> Dict[str, object]:
        """Prepare response data."""
        return {
            "request": output_dto.change_subcription_request,
        }
