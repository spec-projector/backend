from constance.admin import Config
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_exempt

from apps.billing.admin.api.views import BillingTariffAutocompleteView
from gql import get_api_graphql_view, get_graphql_view

admin.site.site_header = _("VN__ADMIN_DASHBOARD")
constance_admin = admin.site._registry.get(Config)  # noqa: WPS437

admin_urls = (
    path(
        "configuration/",
        constance_admin.admin_site.admin_view(constance_admin.changelist_view),
        name="configuration",
    ),
    path(
        "billing/tariff/autocomplete/",
        BillingTariffAutocompleteView.as_view(),
    ),
    *admin.site.urls[0],
)

urlpatterns = [
    path("ht/", include("health_check.urls", namespace="ht")),
    path("graphql/", get_graphql_view()),
    path("api/graphql", csrf_exempt(get_api_graphql_view())),
    path("api/", include("apps.users.pages.urls", namespace="api")),
    path(
        "webhooks/",
        include(
            "apps.billing.webhooks.urls",
            namespace="webhooks",
        ),
    ),
    path("admin_tools/", include("jnt_admin_tools.urls")),  # noqa: DJ05
    path("admin/", include((admin_urls, "admin"))),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
