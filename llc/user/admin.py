from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser

    fieldsets = UserAdmin.fieldsets + (
        ("Role", {"fields": ("is_instructor", "is_student")}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Role", {"fields": ("is_instructor", "is_student")}),
    )

    list_display = ("username", "email", "is_instructor", "is_student", "is_staff")