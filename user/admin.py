from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("Roles & Profile", {"fiels": ("is_instructor", "is_student", "profile_image")})
    )

    list_display = ("username", "is_insturctor", "is_student", "is_staff")


