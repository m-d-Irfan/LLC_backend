from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from django.core.mail import send_mail
from django.conf import settings

from course.models import Course, Lesson
from enrollment.models import LessonProgress, Enrollment
from .models import Certificate
from .serializers import CertificateSerializer
from user.permissions import IsStudent


class FinishCourseView(APIView):
    permission_classes = [IsStudent]

    def post(self, request):
        course_id = request.data.get("course")

        # 1. Does this course exist?
        try:
            course = Course.objects.get(pk=course_id)
        except Course.DoesNotExist:
            return Response(
                {"error": "Course not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        # 2. Is the student enrolled?
        is_enrolled = Enrollment.objects.filter(
            student=request.user,
            course=course,
            is_active=True
        ).exists()

        if not is_enrolled:
            return Response(
                {"error": "You are not enrolled in this course"},
                status=status.HTTP_403_FORBIDDEN
            )

        # 3. Count total lessons in this course
        total_lessons = Lesson.objects.filter(
            module__course=course      # traverse: lesson → module → course
        ).count()

        # 4. Count how many this student completed
        completed_lessons = LessonProgress.objects.filter(
            student=request.user,
            lesson__module__course=course   # same traversal
        ).count()

        # 5. Are all lessons done?
        if completed_lessons < total_lessons:
            return Response(
                {
                    "error": "Course not completed yet",
                    "completed": completed_lessons,
                    "total": total_lessons
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # 6. Create certificate (get_or_create avoids duplicates)
        certificate, created = Certificate.objects.get_or_create(
            student=request.user,
            course=course
        )

        # 7. Send email only if newly created
        if created:
            send_mail(
                subject=f"Congratulations! You completed {course.title}",
                message=f"""
Hi {request.user.first_name},

Congratulations on completing {course.title}!

Your certificate ID: {certificate.certificate_id}
You can download your certificate from your dashboard.

— EduCore AI Team
                """,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[request.user.email],
                fail_silently=True,   # won't crash if email fails
            )

        # 8. Return certificate data
        serializer = CertificateSerializer(certificate)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CertificateListView(generics.ListAPIView):
    permission_classes = [IsStudent]
    serializer_class = CertificateSerializer

    def get_queryset(self):
        return Certificate.objects.filter(
            student=self.request.user
        ).select_related("course")