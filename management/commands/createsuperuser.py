from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os

class Command(BaseCommand):
    help = "Creates a superuser if none exists"

    def handle(self, *args, **options):
        User = get_user_model()
        if not User.objects.filter(is_superuser=True).exists():
            username = os.environ.get("DJANGO_SUPERUSER_USERNAME", "educorellc")
            email    = os.environ.get("DJANGO_SUPERUSER_EMAIL",    "educore.llc@gmail.com")
            password = os.environ.get("DJANGO_SUPERUSER_PASSWORD", "llc2026educore")
            User.objects.create_superuser(username=username, email=email, password=password)
            print(f"Superuser '{username}' created.")
        else:
            print("Superuser already exists.")