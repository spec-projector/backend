from django.contrib import admin

from apps.core.admin.base import BaseModelAdmin
from apps.projects.models import Project


@admin.register(Project)
class ProjectAdmin(BaseModelAdmin):
    list_display = ('title', 'created_at')
    search_fields = ('title',)
