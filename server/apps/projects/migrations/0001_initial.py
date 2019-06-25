# Generated by Django 2.2.2 on 2019-06-25 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(help_text='HT__TITLE', max_length=255, verbose_name='VN__TITLE')),
            ],
            options={
                'verbose_name': 'VN__PROJECT',
                'verbose_name_plural': 'VN__PROJECTS',
                'ordering': ('-created_at',),
            },
        ),
    ]