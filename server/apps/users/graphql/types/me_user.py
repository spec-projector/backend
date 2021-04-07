import graphene
from graphql import ResolveInfo

from apps.billing.graphql.types import SubscriptionType
from apps.billing.graphql.types.change_subscription_request import (
    ChangeSubscriptionRequestType,
)
from apps.billing.logic.queries.change_subscription_request import (
    active as change_subscription_request,
)
from apps.billing.logic.queries.subscription import active as subscription


class MeUserType(graphene.ObjectType):
    """Me user graphql type."""

    id = graphene.ID()
    first_name = graphene.String()
    last_name = graphene.String()
    email = graphene.String()
    is_staff = graphene.Boolean()
    is_active = graphene.Boolean()
    avatar = graphene.String()
    last_login = graphene.DateTime()
    subscription = graphene.Field(SubscriptionType)
    change_subscription_request = graphene.Field(ChangeSubscriptionRequestType)

    def resolve_subscription(self, info: ResolveInfo):  # noqa: WPS110
        """Returns user subscription."""
        return subscription.Query().execute(subscription.InputDto(user=self))

    def resolve_change_subscription_request(
        self,
        info: ResolveInfo,  # noqa: WPS110
    ):
        """Returns user change subscription request."""
        return change_subscription_request.Query().execute(
            change_subscription_request.InputDto(user=self),
        )
