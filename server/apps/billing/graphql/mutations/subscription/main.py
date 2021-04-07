from apps.billing.graphql.mutations.subscription import change


class SubscriptionMutations:
    """All subscription mutations."""

    change_subscription = change.ChangeSubscriptionMutation.Field()
