from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):

    username = models.CharField(
        max_length=150, verbose_name="username", help_text="Enter your username", null=True, blank=True
    )
    email = models.EmailField(unique=True, verbose_name="email", help_text="Enter your email")
    first_name = models.CharField(
        max_length=150, verbose_name="first name", help_text="Enter your first name username", null=True, blank=True
    )
    last_name = models.CharField(
        max_length=150, verbose_name="last name", help_text="Enter your last name username", null=True, blank=True
    )
    phone_number = models.CharField(
        max_length=30, verbose_name="phone number", help_text="Enter your phone number", null=True, blank=True
    )
    city = models.CharField(max_length=150, verbose_name="city", help_text="Enter your city", null=True, blank=True)
    avatar = models.ImageField(
        upload_to="users/", verbose_name="photo", help_text="Upload your photo", null=True, blank=True
    )
    is_staff = models.BooleanField(
        default=False, verbose_name="staff", help_text="Select whether user can act as admin"
    )
    is_active = models.BooleanField(
        default=True, verbose_name="active", help_text="Select whether user can use the service"
    )
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username if self.username else self.email

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"
