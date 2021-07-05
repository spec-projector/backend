import typing as ty
from dataclasses import dataclass

from django import forms
from django.apps import apps
from django.contrib import admin
from django.contrib.admin.widgets import AutocompleteSelect
from django.db import models


@dataclass
class MockRelation:
    """Mock relation for autocomplete select widget."""

    model: models.Model
    name: str
    remote_field: ty.Optional[object] = None


class ForeignConfigField(forms.ModelChoiceField):
    """Foreign config field."""

    def __init__(self, model: str, *args, **kwargs) -> None:
        """Init foreign config field."""
        current_model = apps.get_model(*model.split("."))

        kwargs["queryset"] = current_model.objects.all()
        kwargs["widget"] = self._get_widget(current_model)
        kwargs["required"] = False

        super().__init__(*args, **kwargs)

    def _get_widget(self, current_model) -> AutocompleteSelect:
        """Get widget for current model."""
        mock_rel = MockRelation(current_model, "default_tariff")
        mock_rel.remote_field = mock_rel

        widget = AutocompleteSelect(
            field=mock_rel,
            admin_site=admin.site,
        )
        widget.get_url = self._get_url

        return widget

    def _get_url(self) -> str:
        """Get autocomplete url."""
        return "/admin/billing/tariff/autocomplete/"
