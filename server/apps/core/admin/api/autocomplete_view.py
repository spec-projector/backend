from django.contrib import admin
from django.contrib.admin.views.autocomplete import AutocompleteJsonView
from django.core.exceptions import PermissionDenied
from django.db import models
from django.http import JsonResponse
from rest_framework import serializers


class AutocompleteSerializer(serializers.Serializer):
    """Autocomplete serializer."""

    id = serializers.IntegerField()
    text = serializers.SerializerMethodField(method_name="get_tariff_present")

    def get_tariff_present(self, instance) -> str:
        """Get text as object present."""
        return str(instance)


class BaseAutocompleteView(AutocompleteJsonView):
    """Billing tariff autocomplete view."""

    model: models.Model

    def __init__(self, *args, **kwargs) -> None:
        """Init view."""
        super().__init__(*args, **kwargs)
        self.model_admin = self.get_model_admin()

    def get(self, request, *args, **kwargs) -> JsonResponse:
        """Return a JsonResponse with search results of the form."""
        if not self.has_perm(request):
            raise PermissionDenied

        self.term = request.GET.get("term", "")
        self.object_list = self.get_queryset()

        context = self.get_context_data()
        return JsonResponse(
            {
                "results": AutocompleteSerializer(
                    instance=context["object_list"],
                    many=True,
                ).data,
                "pagination": {
                    "more": context["page_obj"].has_next(),
                },
            },
        )

    def get_queryset(self) -> models.QuerySet:
        """Return queryset based on ModelAdmin.get_search_results()."""
        queryset = self.model_admin.get_queryset(self.request)
        queryset, search_use_distinct = self.model_admin.get_search_results(
            self.request,
            queryset,
            self.term,
        )
        if search_use_distinct:
            queryset = queryset.distinct()

        return queryset.filter(is_active=True)

    def get_model_admin(self) -> admin.ModelAdmin:  # noqa: WPS615
        """Get model admin for autocomplete view."""
        return admin.site._registry.get(self.model)  # noqa: WPS437
