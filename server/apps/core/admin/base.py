from django import forms
from django.contrib import admin
from django.contrib.contenttypes.admin import GenericStackedInline, GenericTabularInline

from apps.core.admin.list_filters import AutocompleteChangeListFilter
from apps.core.admin.mixins import AdminFormFieldsOverridesMixin


class BaseModelAdmin(AdminFormFieldsOverridesMixin,
                     admin.ModelAdmin):
    list_per_page = 20

    def changelist_view(self, request, extra_context=None):
        changelist_view = super().changelist_view(request, extra_context=extra_context)
        self._update_media(changelist_view)
        return changelist_view

    def _update_media(self, changelist):
        if not hasattr(changelist.context_data['cl'], 'filter_specs') or not changelist.context_data['cl'].filter_specs:
            return

        for list_filter in changelist.context_data['cl'].filter_specs:
            if isinstance(list_filter, AutocompleteChangeListFilter):
                self._update_static(changelist, list_filter)

    @staticmethod
    def _update_static(changelist, filter):
        for js in filter.media._js_lists:
            changelist.context_data['media']._js_lists.append(js)

        for css in filter.media._css_lists:
            changelist.context_data['media']._css_lists.append(css)

    class Media:
        pass


class BaseStackedInline(AdminFormFieldsOverridesMixin,
                        admin.StackedInline):
    extra = 0
    show_change_link = True


class BaseTabularInline(AdminFormFieldsOverridesMixin,
                        admin.TabularInline):
    extra = 0
    show_change_link = True


class BaseGenericStackedInline(AdminFormFieldsOverridesMixin,
                               GenericStackedInline):
    extra = 0
    show_change_link = True


class BaseGenericTabularInline(AdminFormFieldsOverridesMixin,
                               GenericTabularInline):
    extra = 0
    show_change_link = True


class BaseModelForm(forms.ModelForm):
    pass
