import os

from django.core.management import BaseCommand
from dotenv import load_dotenv

from users.models import User


class Command(BaseCommand):
    """Custom command for creating superuser."""

    def handle(self, *args, **options):
        load_dotenv()
        user = User.objects.create(email=os.getenv("SUPERUSER_EMAIL"))
        user.set_password(os.getenv("SUPERUSER_PASSWORD"))
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save()
