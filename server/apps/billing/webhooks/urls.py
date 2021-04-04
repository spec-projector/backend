from django.urls import path

from apps.billing.webhooks import views

app_name = "billing"

urlpatterns = [
    path(
        "cloud_payments",
        views.CloudPaymentsWebhookView.as_view(),
        name="webhook-cloud_payments",
    ),
]
