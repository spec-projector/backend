from constance.admin import Config
from constance.admin import ConstanceAdmin as BaseConstanceAdmin
from django.contrib import admin

from apps.core.admin.forms import ConstanceForm

admin.site.unregister((Config,))


@admin.register(Config)
class ConstanceAdmin(BaseConstanceAdmin):
    """Constance admin."""

    change_list_form = ConstanceForm
