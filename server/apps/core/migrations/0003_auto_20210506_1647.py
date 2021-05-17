# Generated by Django 3.1.7 on 2021-05-06 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20210303_1756'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailmessage',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, help_text='HT__CREATED_AT', verbose_name='VN__CREATED_AT'),
        ),
        migrations.AlterField(
            model_name='emailmessage',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, help_text='HT__UPDATED_AT', verbose_name='VN__UPDATED_AT'),
        ),
    ]