import uuid
from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class Certificate(models.Model):
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="certificates"
    )
    course = models.ForeignKey(
        "course.Course",
        on_delete=models.CASCADE,
        related_name="certificates"
    )
    issued_at = models.DateTimeField(auto_now_add=True)
    certificate_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)

    class Meta:
        unique_together = ["student", "course"]

    def __str__(self):
        return f"{self.student} - {self.course} certificate"