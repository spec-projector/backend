from django.contrib import admin

from apps.core.admin.base import BaseModelAdmin
from ..models import Project


@admin.register(Project)
class TeamAdmin(BaseModelAdmin):
    list_display = ('title', 'created_at')
    search_fields = ('title',)
