# -*- coding: utf-8 -*-

from django.db import migrations

from apps.core.utils.hash import generate_md5


def update_project_uids(apps, schema_editor):
    Project = apps.get_model('projects', 'project')  # noqa: N806

    for project in Project.objects.filter(uid=''):
        project.uid = generate_md5()
        project.save(update_fields=['uid'])


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0004_project_uid'),
    ]

    operations = [
        migrations.RunPython(update_project_uids),
    ]
