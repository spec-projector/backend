# Generated by Django 3.1.10 on 2021-05-28 07:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0030_auto_20210524_1429'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='projectasset',
            name='old_file',
        ),
    ]
