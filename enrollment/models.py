from django.db import models
from django.conf import settings
from django.utils import timezone

User = settings.AUTH_USER_MODEL

class Enrollment(models.Model):
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="enrollments" 
    )
    course = models.ForeignKey(
        "course.Course",     
        on_delete=models.CASCADE,
        related_name="course_enrollments"   
    )
    enrolled_at = models.DateTimeField(auto_now_add=True)   
    is_active = models.BooleanField(default=True)   

    class Meta:
        unique_together = ["student", "course"]

    def __str__(self):
        return f"{self.student} enrolled in {self.course}"

class LessonProgress(models.Model):
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name= "lesson_progress"
    )
    lesson = models.ForeignKey(
        "course.Lesson",
        on_delete=models.CASCADE,
        related_name="lesson_progress"
        
    )
    completed_at = models.DateTimeField(auto_now_add=True)
    is_complete = models.BooleanField(default=False)
    class Meta:
        unique_together = ["student", "lesson"]






