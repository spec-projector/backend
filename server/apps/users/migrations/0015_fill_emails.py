# Generated by Django 3.1.7 on 2021-04-02 13:54

from django.db import migrations


def fill_emails(apps, schema_editor):
    User = apps.get_model("users", "User")  # noqa: N806

    for user in User.objects.filter(email=""):
        user.email = "{0}@mail.auto".format(user.login)
        user.save()


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0014_auto_20210402_1239'),
    ]

    operations = [
        migrations.RunPython(
            fill_emails, migrations.RunPython.noop,
        ),
    ]