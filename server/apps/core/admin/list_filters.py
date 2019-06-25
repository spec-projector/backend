from django import forms
from django.contrib import admin
from django.contrib.admin.utils import get_fields_from_path
from django.contrib.admin.widgets import AutocompleteSelectMultiple, AutocompleteSelect
from django.utils.safestring import mark_safe


class ErrorAutocompleteFilter(Exception):
    pass


class AutocompleteChangeListFilter(admin.SimpleListFilter):
    title = 'List filter'
    parameter_name = None
    template = 'core/filters/list_filter.html'
    is_multiple = None
    custom_model = None

    def __init__(self, request, params, model, model_admin):
        super().__init__(request, params, model, model_admin)

        if not self.parameter_name:
            raise ErrorAutocompleteFilter('Parameter name is required')

        if self.custom_model:
            model = self.custom_model

        field_for_model = get_fields_from_path(model, self.parameter_name)[-1]

        if self.is_multiple is None:
            self.is_multiple = field_for_model.many_to_many

        self.request = request

        rel = field_for_model.remote_field if field_for_model.remote_field else field_for_model
        widget = self.get_widget_class()(rel, admin.site)
        field = self.get_field_class()(queryset=self.get_field_queryset(model), widget=widget, required=False)

        value = self.get_value(request)

        attrs = {
            'is_list_filter': True,
            'data-parameter': self.parameter_name,
        }

        self.rendered_widget = field.widget.render(name=self.parameter_name, value=value, attrs=attrs)
        self.rendered_widget = self.rendered_widget.replace('class="admin-autocomplete"', 'class="filter-autocomplete"')
        self.rendered_widget = mark_safe(self.rendered_widget)

        self.media = self.get_media(field.widget)

    def lookups(self, request, model_admin):
        return (('__id__in', 'in list'),)

    def queryset(self, request, queryset):
        value = self.get_value(request)

        if value:
            lookup, _ = self.lookups(request, None)[0]

            query = {
                f'{self.parameter_name}{lookup}': value
            }

            queryset = queryset.filter(**query)

        return queryset

    def get_value(self, request):
        return request.GET.getlist(self.parameter_name)

    def get_field_queryset(self, model):
        return get_fields_from_path(model, self.parameter_name)[-1].target_field.model.objects.all()

    def get_widget_class(self):
        return AutocompleteSelectMultiple if self.is_multiple else AutocompleteSelect

    def get_field_class(self):
        return forms.ModelMultipleChoiceField if self.is_multiple else forms.ModelChoiceField

    def get_media(self, widget):
        media = widget.media
        media._js_lists[0] = tuple(list(media._js_lists[0]) + list(self.Media.js))

        return media

    class Media:
        js = ('js/core/filters/changelist_filter.js',)
