import graphene
from graphql import ResolveInfo

from apps.billing.graphql.types import SubscriptionType
from apps.billing.logic.queries.subscription import active


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

    def resolve_subscription(self, info: ResolveInfo):  # noqa: WPS110
        """Returns user subscription."""
        return active.Query().execute(active.InputDto(user=self))
