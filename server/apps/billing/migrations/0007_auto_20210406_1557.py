# Generated by Django 3.1.7 on 2021-04-06 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0006_auto_20210406_1555'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription',
            name='created',
            field=models.DateTimeField(auto_now_add=True, help_text='HT__CREATED', verbose_name='VN__CREATED'),
        ),
    ]