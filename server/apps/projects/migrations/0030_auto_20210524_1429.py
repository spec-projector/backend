# Generated by Django 3.1.10 on 2021-05-24 11:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0029_projectasset_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectasset',
            name='project',
            field=models.ForeignKey(help_text='HT__PROJECT', null=True, on_delete=django.db.models.deletion.CASCADE, to='projects.project', verbose_name='VN__PROJECT'),
        ),
    ]
