from constance.admin import ConstanceForm as BaseConstanceForm
from django.contrib import admin
from django.contrib.admin.widgets import AutocompleteSelect
from django.forms import ModelChoiceField

from apps.billing.models import Tariff


class MockRelation:
    """Mock relation for autocomplete select widget."""

    model = Tariff


class ConstanceForm(BaseConstanceForm):
    """Constance form."""

    def __init__(self, *args, **kwargs):
        """Initialize form."""
        super().__init__(*args, **kwargs)
        self._update_default_tariff()

    def _update_default_tariff(self) -> None:
        """Update default tariff field."""
        field_name = "DEFAULT_TARIFF"

        self.fields[field_name] = ModelChoiceField(
            queryset=Tariff.objects.all(),
            widget=AutocompleteSelect(rel=MockRelation, admin_site=admin.site),
            required=False,
        )
