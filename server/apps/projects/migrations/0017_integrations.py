# Generated by Django 3.1.5 on 2021-02-08 11:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0016_auto_20210112_1402'),
    ]

    operations = [
        migrations.CreateModel(
            name='GitLabIntegration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(blank=True, default='', help_text='HT__TOKEN', max_length=128, verbose_name='VN__TOKEN')),
                ('project', models.OneToOneField(help_text='HT__PROJECT', on_delete=django.db.models.deletion.CASCADE, to='projects.project', verbose_name='VN__PROJECT')),
            ],
            options={
                'verbose_name': 'VN__GITLAB_INTEGRATION',
                'verbose_name_plural': 'VN__GITLAB_INTERGRATIONS',
            },
        ),
        migrations.CreateModel(
            name='GitHubIntegration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(blank=True, default='', help_text='HT__TOKEN', max_length=128, verbose_name='VN__TOKEN')),
                ('project', models.OneToOneField(help_text='HT__PROJECT', on_delete=django.db.models.deletion.CASCADE, to='projects.project', verbose_name='VN__PROJECT')),
            ],
            options={
                'verbose_name': 'VN__GITHUB_INTEGRATION',
                'verbose_name_plural': 'VN__GITHUB_INTERGRATIONS',
            },
        ),
        migrations.CreateModel(
            name='FigmaIntegration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(blank=True, default='', help_text='HT__TOKEN', max_length=128, verbose_name='VN__TOKEN')),
                ('project', models.OneToOneField(help_text='HT__PROJECT', on_delete=django.db.models.deletion.CASCADE, to='projects.project', verbose_name='VN__PROJECT')),
            ],
            options={
                'verbose_name': 'VN__FIGMA_INTEGRATION',
                'verbose_name_plural': 'VN__FIGMA_INTERGRATIONS',
            },
        ),
    ]
