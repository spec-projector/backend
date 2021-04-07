from apps.billing.graphql.mutations import subscription


class BillingMutations(
    subscription.SubscriptionMutations,
):
    """All billing mutations."""
