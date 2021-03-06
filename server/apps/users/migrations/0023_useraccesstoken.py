# Generated by Django 3.1.10 on 2021-06-11 15:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0022_user_last_activity'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserAccessToken',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='HT__NAME', max_length=256, verbose_name='VN__NAME')),
                ('key', models.CharField(db_index=True, help_text='HT__KEY', max_length=64, unique=True, verbose_name='VN__KEY')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='HT__CREATED_AT', verbose_name='VN__CREATED_AT')),
                ('user', models.ForeignKey(help_text='HT__USER', on_delete=django.db.models.deletion.CASCADE, related_name='access_tokens', to=settings.AUTH_USER_MODEL, verbose_name='VN__USER')),
            ],
            options={
                'verbose_name': 'VN__USER_ACCESS_TOKEN',
                'verbose_name_plural': 'VN__USER_ACCESS_TOKENS',
            },
        ),
    ]
