# Generated by Django 2.2.8 on 2019-12-18 07:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0003_project_description"),
    ]

    operations = [
        migrations.AddField(
            model_name="project",
            name="uid",
            field=models.CharField(default="", help_text="HT__UID", max_length=32, verbose_name="VN__UID"),
        ),
    ]
