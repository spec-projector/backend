# Generated by Django 3.1.7 on 2021-04-02 14:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0016_auto_20210402_1737'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='login',
        ),
    ]
