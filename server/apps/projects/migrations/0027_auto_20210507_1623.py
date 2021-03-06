# Generated by Django 3.1.10 on 2021-05-07 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0026_auto_20210507_1620'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='public_role',
            field=models.CharField(choices=[('VIEWER', 'CH__VIEWER'), ('EDITOR', 'CH__EDITOR')], default='VIEWER', help_text='HT__PUBLIC_ROLE', max_length=32, verbose_name='VN__PUBLIC_ROLE'),
        ),
    ]
