# Generated by Django 3.1.10 on 2021-06-09 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0021_remove_user_old_avatar'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='last_activity',
            field=models.DateTimeField(blank=True, help_text='HT__LAST_ACTIVITY', null=True, verbose_name='VN__LAST_ACTIVITY'),
        ),
    ]
