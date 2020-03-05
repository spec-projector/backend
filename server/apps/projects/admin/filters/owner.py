# -*- coding: utf-8 -*-

from admin_tools.autocomplete_filter import AutocompleteFilter


class OwnerAutocompleteFilter(AutocompleteFilter):
    """Owner filter."""

    title = "Owner"
    field_name = "owner"
