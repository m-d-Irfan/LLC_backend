#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate

# Create superuser from environment variables if it doesn't exist
python manage.py shell << 'EOF'
from django.contrib.auth import get_user_model
User = get_user_model()
import os

username = os.environ.get("DJANGO_SUPERUSER_USERNAME")
password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")
email    = os.environ.get("DJANGO_SUPERUSER_EMAIL")

if username and password:
    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(username=username, password=password, email=email or "")
        print(f"Superuser '{username}' created.")
    else:
        print(f"Superuser '{username}' already exists.")
EOF
