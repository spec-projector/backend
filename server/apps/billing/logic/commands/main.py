from apps.billing.logic.commands.subscription import change, payment_webhook

COMMANDS = (
    (
        payment_webhook.Command,
        payment_webhook.CommandHandler,
    ),
    (change.Command, change.CommandHandler),
)
