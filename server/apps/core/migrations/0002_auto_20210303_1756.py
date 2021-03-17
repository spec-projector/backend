# Generated by Django 3.1.7 on 2021-03-03 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailmessage',
            name='status',
            field=models.CharField(choices=[('created', 'CH__CREATED'), ('ready', 'CH__READY'), ('sending', 'CH__SENDING'), ('sent', 'CH__SENT'), ('error', 'CH__ERROR')], db_index=True, default='created', help_text='HT__EMAIL_MESSAGE_STATUS', max_length=50, verbose_name='VN__EMAIL_MESSAGE_STATUS'),
        ),
    ]