# Generated by Django 2.2.8 on 2019-12-19 08:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0007_migrate_id_int_to_str'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='uid',
        ),
    ]
