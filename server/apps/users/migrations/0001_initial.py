# -*- coding: utf-8 -*-
# Generated by Django 2.2 on 2019-04-26 11:41


from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("auth", "0011_update_proxy_permissions"),
    ]

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True,
                                        serialize=False, verbose_name="ID")),
                ("password",
                 models.CharField(max_length=128, verbose_name="password")),
                ("last_login", models.DateTimeField(blank=True, null=True,
                                                    verbose_name="last login")),
                ("is_superuser", models.BooleanField(
                    default=False,
                    help_text="Designates that this user has all permissions without explicitly assigning them.",
                    verbose_name="superuser status",
                )),
                ("login", models.CharField(blank=True, help_text="HT__LOGIN",
                                           max_length=150, null=True,
                                           unique=True,
                                           verbose_name="VN__LOGIN")),
                ("name", models.CharField(blank=True, help_text="HT__NAME",
                                          max_length=150, null=True,
                                          unique=True,
                                          verbose_name="VN__NAME")),
                ("email", models.EmailField(blank=True, help_text="HT__EMAIL",
                                            max_length=150, null=True,
                                            unique=True,
                                            verbose_name="VN__EMAIL")),
                ("is_staff",
                 models.BooleanField(default=True, help_text="HT__IS_STAFF",
                                     verbose_name="VN__IS_STAFF")),
                ("is_active",
                 models.BooleanField(default=True, help_text="HT__IS_ACTIVE",
                                     verbose_name="VN__IS_ACTIVE")),
                ("groups", models.ManyToManyField(
                    blank=True,
                    help_text="The groups this user belongs to. A user will "
                              + "get all permissions granted to each of their "
                              + "groups.",
                    related_name="user_set",
                    related_query_name="user",
                    to="auth.Group",
                    verbose_name="groups",
                )),
                ("user_permissions", models.ManyToManyField(
                    blank=True,
                    help_text="Specific permissions for this user.",
                    related_name="user_set",
                    related_query_name="user",
                    to="auth.Permission",
                    verbose_name="user permissions",
                )),
            ],
            options={
                "verbose_name": "VN__USER",
                "verbose_name_plural": "VN__USERS",
                "ordering": ("login",),
            },
        ),
        migrations.CreateModel(
            name="Token",
            fields=[
                ("key", models.CharField(max_length=40, primary_key=True,
                                         serialize=False, verbose_name="Key")),
                ("created", models.DateTimeField(auto_now_add=True,
                                                 verbose_name="Created")),
                ("user",
                 models.ForeignKey(on_delete=models.deletion.CASCADE,
                                   to=settings.AUTH_USER_MODEL)),
            ],
            options={
                "verbose_name": "VN__TOKEN",
                "verbose_name_plural": "VN__TOKENS",
            },
        ),
    ]
