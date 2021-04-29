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
from apps.core.logic import queries
from apps.core.utils.media import get_absolute_path


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
        return queries.execute_query(
            change_subscription_request.GetActiveSubscriptionQuery(
                user=self,
            ),
        )

    def resolve_avatar(self, info):  # noqa: WPS110
        """Resolve image absolute path."""
        return get_absolute_path(self.avatar)
