# Generated by Django 3.1.7 on 2021-04-10 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0017_auto_20210410_1752'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription',
            name='merchant_id',
            field=models.CharField(blank=True, default='', help_text='HT__MERCHANT_ID', max_length=128, verbose_name='VN__MERCHANT_ID'),
        ),
    ]