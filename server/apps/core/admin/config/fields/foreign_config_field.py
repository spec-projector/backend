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


class ForeignConfigField(forms.ModelChoiceField):
    """Foreign config field."""

    def __init__(self, model: str, *args, **kwargs):
        """Init foreign config field."""
        current_model = apps.get_model(*model.split("."))

        kwargs["queryset"] = current_model.objects.all()
        kwargs["widget"] = AutocompleteSelect(
            rel=MockRelation(current_model),
            admin_site=admin.site,
        )
        kwargs["required"] = False

        super().__init__(*args, **kwargs)
