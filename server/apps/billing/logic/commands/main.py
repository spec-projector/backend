from apps.billing.logic.commands.subscription import change, payment_webhook

COMMANDS = (
    (
        payment_webhook.HandlePaymentWebhookCommand,
        payment_webhook.CommandHandler,
    ),
    (change.ChangeSubscriptionCommand, change.CommandHandler),
)
