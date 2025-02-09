from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone

from config.settings import PAYMENT_METHODS
from courses.models import Course, Lesson


class User(AbstractUser):

    username = models.CharField(
        max_length=150, verbose_name="username", help_text="Enter your username", null=True, blank=True
    )
    email = models.EmailField(unique=True, verbose_name="email", help_text="Enter your email")
    first_name = models.CharField(
        max_length=150, verbose_name="first name", help_text="Enter your first name", null=True, blank=True
    )
    last_name = models.CharField(
        max_length=150, verbose_name="last name", help_text="Enter your last name", null=True, blank=True
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


class Payment(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        related_name="payments",
        verbose_name="user",
        help_text="Select the user",
    )
    payment_date = models.DateTimeField(
        verbose_name="payment date", help_text="Enter the payment date", auto_now_add=True
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.DO_NOTHING,
        related_name="payments",
        verbose_name="course",
        help_text="Select the course",
        null=True,
        blank=True,
    )
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.DO_NOTHING,
        related_name="payments",
        verbose_name="lesson",
        help_text="Select the lesson",
        null=True,
        blank=True,
    )
    payment_amount = models.DecimalField(
        verbose_name="payment amount",
        help_text="Enter the payment amount",
        decimal_places=2,
        max_digits=9,
        validators=[MinValueValidator(0)],
    )
    payment_method = models.CharField(
        max_length=13, choices=PAYMENT_METHODS, verbose_name="payment_method", help_text="Choose the payment method"
    )

    def __str__(self):
        return f"Payment for {self.course} by {self.user.email}"

    class Meta:
        verbose_name = "payment"
        verbose_name_plural = "payments"
