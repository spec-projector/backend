from typing import Dict, Optional

import graphene
from graphql import ResolveInfo

from apps.billing.graphql.types.change_subscription_request import (
    ChangeSubscriptionRequestType,
)
from apps.billing.logic.commands.subscription import (
    change as change_subscription,
)
from apps.core.graphql.mutations import BaseCommandMutation
from apps.core.logic import commands


class ChangeSubscriptionInput(graphene.InputObjectType):
    """Input for create project asset."""

    tariff = graphene.ID(required=True)
    hash = graphene.String(required=True)


class ChangeSubscriptionMutation(BaseCommandMutation):
    """Change subscription mutation."""

    class Meta:
        auth_required = True

    class Arguments:
        input = graphene.Argument(  # noqa: WPS125
            ChangeSubscriptionInput,
            required=True,
        )

    request = graphene.Field(ChangeSubscriptionRequestType)

    @classmethod
    def build_command(
        cls,
        root: Optional[object],
        info: ResolveInfo,  # noqa: WPS110
        **kwargs,
    ) -> commands.ICommand:
        """Build command."""
        input_dto = kwargs["input"]
        return change_subscription.ChangeSubscriptionCommand(
            user=info.context.user,  # type: ignore
            tariff=input_dto["tariff"],
            hash=input_dto["hash"],
        )

    @classmethod
    def get_response_data(
        cls,
        root: Optional[object],
        info: ResolveInfo,  # noqa: WPS110
        command_result: change_subscription.ChangeSubscriptionCommandResult,
    ) -> Dict[str, object]:
        """Prepare response data."""
        return {
            "request": command_result.change_subcription_request,
        }
