# Generated by Django 3.1.7 on 2021-04-16 12:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0018_auto_20210410_1805'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tariff',
            name='is_default',
        ),
    ]