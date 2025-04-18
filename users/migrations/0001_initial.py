# Generated by Django 5.1.4 on 2025-01-11 19:22

import django.contrib.auth.models
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                ("last_login", models.DateTimeField(blank=True, null=True, verbose_name="last login")),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                (
                    "username",
                    models.CharField(
                        blank=True, help_text="Enter your username", max_length=150, null=True, verbose_name="username"
                    ),
                ),
                (
                    "email",
                    models.EmailField(help_text="Enter your email", max_length=254, unique=True, verbose_name="email"),
                ),
                (
                    "first_name",
                    models.CharField(
                        blank=True,
                        help_text="Enter your first name username",
                        max_length=150,
                        null=True,
                        verbose_name="first name",
                    ),
                ),
                (
                    "last_name",
                    models.CharField(
                        blank=True,
                        help_text="Enter your last name username",
                        max_length=150,
                        null=True,
                        verbose_name="last name",
                    ),
                ),
                (
                    "phone_number",
                    models.CharField(
                        blank=True,
                        help_text="Enter your phone number",
                        max_length=30,
                        null=True,
                        verbose_name="phone number",
                    ),
                ),
                (
                    "city",
                    models.CharField(
                        blank=True, help_text="Enter your city", max_length=150, null=True, verbose_name="city"
                    ),
                ),
                (
                    "avatar",
                    models.ImageField(
                        blank=True, help_text="Upload your photo", null=True, upload_to="users/", verbose_name="photo"
                    ),
                ),
                (
                    "is_staff",
                    models.BooleanField(
                        default=False, help_text="Select whether user can act as admin", verbose_name="staff"
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True, help_text="Select whether user can use the service", verbose_name="active"
                    ),
                ),
                ("date_joined", models.DateTimeField(default=django.utils.timezone.now)),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "verbose_name": "user",
                "verbose_name_plural": "users",
            },
            managers=[
                ("objects", django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
