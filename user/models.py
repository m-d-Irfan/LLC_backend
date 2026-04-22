import hashlib
from operator import truediv

from django.contrib.auth.models import AbstractUser
from django.db import models

def user_profile_image_path(instance: "CustomUser", filename: str) -> str:
    return f"user_profile/{instance.id}/{filename}"

class InstructorStatus(models.TextChoices):
    PENDING  = "pending",  "Pending"
    APPROVED = "approved", "Approved"
    REJECTED = "rejected", "Rejected"

class CustomUser(AbstractUser):
    is_instructor = models.BooleanField(default=False)
    is_student    = models.BooleanField(default=True)

    # Only meaningful when is_instructor=True
    instructor_status = models.CharField(
        max_length=10,
        choices=InstructorStatus.choices,
        default=InstructorStatus.PENDING,
    )
    # Admins can leave a note when rejecting an instructor
    instructor_rejection_reason = models.TextField(blank=True, default="")

    # profile_image = models.ImageField(upload_to="profiles/", blank=True, null=True)
    profile_image = models.ImageField(
        upload_to=user_profile_image_path,
        null=True,
        blank=True,
    )

    def save(self, *args, **kwargs):
        # Ensure at least one role is true (safety)
        if not self.is_instructor and not self.is_student:
            self.is_student = True
        super().save(*args, **kwargs)

    # @property
    # def avatar_url(self) -> str:
    #     """
    #     Frontend-friendly avatar URL.
    #     Priority:
    #     1) uploaded profile_image
    #     2) gravatar based on email (no auth needed)
    #     """
    #     if self.profile_image:
    #         try:
    #             return self.profile_image.url
    #         except Exception:
    #             pass

    #     email = (self.email or "").strip().lower()
    #     email_hash = hashlib.md5(email.encode("utf-8")).hexdigest()
    #     # 'identicon' generates a nice default if no gravatar exists
    #     return f"https://www.gravatar.com/avatar/{email_hash}?d=identicon"