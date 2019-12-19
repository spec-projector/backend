# -*- coding: utf-8 -*-

import uuid

from django.db import migrations, models

MODEL_NAME = 'project'


def fill_project_uuid(apps, schema_editor):
    db_alias = schema_editor.connection.alias
    Project = apps.get_model('projects', MODEL_NAME)  # noqa: N806

    for project in Project.objects.using(db_alias).all():
        project.uuid = uuid.uuid4()
        project.save()


class Migration(migrations.Migration):
    dependencies = [
        ('projects', '0006_update_default_uid_'),
    ]

    operations = [
        migrations.AddField(
            model_name=MODEL_NAME,
            name='uuid',
            field=models.UUIDField(null=True),
        ),
        migrations.RunPython(
            fill_project_uuid,
            migrations.RunPython.noop,
        ),
        migrations.AlterField(
            model_name=MODEL_NAME,
            name='uuid',
            field=models.UUIDField(
                default=uuid.uuid4,
                serialize=False,
                editable=False,
                unique=True,
            ),
        ),
        migrations.RemoveField(MODEL_NAME, 'id'),
        migrations.RenameField(
            model_name=MODEL_NAME,
            old_name='uuid',
            new_name='id'  # noqa: C812
        ),
        migrations.AlterField(
            model_name=MODEL_NAME,
            name='id',
            field=models.UUIDField(
                default=uuid.uuid4,
                editable=False,
                primary_key=True,
                serialize=False,
            ),
        ),
    ]
