from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from course.models import Course
from enrollment.models import Enrollment
# from payment.models import PaymentRecord
# from payment.serializers import AdminPaymentSerializer
from user.permissions import IsAdminUser
from .serializers import (
    AdminUserSerializer,
    AdminCourseSerializer,
    AdminStatsSerializer,
    InstructorApproveSerializer,
    InstructorRejectSerializer,
)
from .emails import (
    send_instructor_approved,
    send_instructor_rejected,
    send_user_deleted,
    send_course_deleted,
)

User = get_user_model()


# ── Dashboard Stats ──────────────────────────────────────────────────────────

class AdminStatsView(APIView):
    """GET /api/admin/stats/ — dashboard overview numbers."""
    permission_classes = [IsAdminUser]

    def get(self, request):
        data = {
            "total_users":          User.objects.count(),
            "total_students":       User.objects.filter(is_student=True).count(),
            "total_instructors":    User.objects.filter(is_instructor=True).count(),
            "pending_instructors":  User.objects.filter(is_instructor=True, instructor_status="pending").count(),
            "total_courses":        Course.objects.count(),
            "published_courses":    Course.objects.filter(is_published=True).count(),
            "pending_payments":     PaymentRecord.objects.filter(is_verified=False).count(),
            "verified_payments":    PaymentRecord.objects.filter(is_verified=True).count(),
        }
        serializer = AdminStatsSerializer(data)
        return Response(serializer.data)


# ── Users ────────────────────────────────────────────────────────────────────

class AdminUserListView(generics.ListAPIView):
    """GET /api/admin/users/ — all users."""
    permission_classes = [IsAdminUser]
    serializer_class = AdminUserSerializer

    def get_queryset(self):
        return User.objects.all().order_by("-date_joined")


class AdminUserDeleteView(APIView):
    """DELETE /api/admin/users/<id>/ — delete user and email them."""
    permission_classes = [IsAdminUser]

    def delete(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        if user.is_staff:
            return Response(
                {"detail": "Cannot delete admin accounts."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        reason  = request.data.get("reason", "")
        email   = user.email
        username = user.username

        user.delete()
        send_user_deleted(email, username, reason)

        return Response({"detail": f"User '{username}' deleted."}, status=status.HTTP_200_OK)


# ── Instructor Approval ───────────────────────────────────────────────────────

class AdminPendingInstructorListView(generics.ListAPIView):
    """GET /api/admin/instructors/pending/ — instructors awaiting approval."""
    permission_classes = [IsAdminUser]
    serializer_class = AdminUserSerializer

    def get_queryset(self):
        return User.objects.filter(
            is_instructor=True,
            instructor_status="pending",
        ).order_by("date_joined")


class AdminAllInstructorListView(generics.ListAPIView):
    """GET /api/admin/instructors/ — all instructors (any status)."""
    permission_classes = [IsAdminUser]
    serializer_class = AdminUserSerializer

    def get_queryset(self):
        return User.objects.filter(is_instructor=True).order_by("-date_joined")


class AdminInstructorApproveView(APIView):
    """POST /api/admin/instructors/<id>/approve/ — approve an instructor."""
    permission_classes = [IsAdminUser]

    def post(self, request, pk):
        try:
            user = User.objects.get(pk=pk, is_instructor=True)
        except User.DoesNotExist:
            return Response({"detail": "Instructor not found."}, status=status.HTTP_404_NOT_FOUND)

        if user.instructor_status == "approved":
            return Response({"detail": "Already approved."}, status=status.HTTP_400_BAD_REQUEST)

        user.instructor_status             = "approved"
        user.instructor_rejection_reason   = ""
        user.save(update_fields=["instructor_status", "instructor_rejection_reason"])

        send_instructor_approved(user)

        return Response(
            {"detail": f"Instructor '{user.username}' approved and notified by email."},
            status=status.HTTP_200_OK,
        )


class AdminInstructorRejectView(APIView):
    """POST /api/admin/instructors/<id>/reject/ — reject an instructor."""
    permission_classes = [IsAdminUser]

    def post(self, request, pk):
        try:
            user = User.objects.get(pk=pk, is_instructor=True)
        except User.DoesNotExist:
            return Response({"detail": "Instructor not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = InstructorRejectSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        reason = serializer.validated_data.get("reason", "")

        user.instructor_status           = "rejected"
        user.instructor_rejection_reason = reason
        user.save(update_fields=["instructor_status", "instructor_rejection_reason"])

        send_instructor_rejected(user, reason)

        return Response(
            {"detail": f"Instructor '{user.username}' rejected and notified by email."},
            status=status.HTTP_200_OK,
        )


# ── Courses ──────────────────────────────────────────────────────────────────

class AdminCourseListView(generics.ListAPIView):
    """GET /api/admin/courses/ — all courses."""
    permission_classes = [IsAdminUser]
    serializer_class = AdminCourseSerializer

    def get_queryset(self):
        return Course.objects.select_related("created_by").order_by("-created_at")


class AdminCourseDeleteView(APIView):
    """DELETE /api/admin/courses/<id>/ — delete a course and email the instructor."""
    permission_classes = [IsAdminUser]

    def delete(self, request, pk):
        try:
            course = Course.objects.select_related("created_by").get(pk=pk)
        except Course.DoesNotExist:
            return Response({"detail": "Course not found."}, status=status.HTTP_404_NOT_FOUND)

        reason           = request.data.get("reason", "")
        course_title     = course.title
        instructor       = course.created_by
        instructor_name  = instructor.get_full_name() or instructor.username

        course.delete()
        send_course_deleted(instructor.email, instructor_name, course_title, reason)

        return Response(
            {"detail": f"Course '{course_title}' deleted and instructor notified."},
            status=status.HTTP_200_OK,
        )


# ── Payments ─────────────────────────────────────────────────────────────────

# class AdminPaymentListView(generics.ListAPIView):
#     """GET /api/admin/payments/ — all payment records."""
#     permission_classes = [IsAdminUser]
#     serializer_class = AdminPaymentSerializer

#     def get_queryset(self):
#         return PaymentRecord.objects.select_related(
#             "student", "course", "verified_by"
#         ).order_by("-submitted_at")


# class AdminPaymentVerifyView(APIView):
#     """
#     PATCH /api/admin/payments/<id>/verify/
#     Toggle is_verified. When set to True, auto-creates the Enrollment.
#     When set to False, removes the Enrollment (revoke access).
#     Body: { "is_verified": true/false }
#     """
#     permission_classes = [IsAdminUser]

#     def patch(self, request, pk):
#         try:
#             payment = PaymentRecord.objects.select_related("student", "course").get(pk=pk)
#         except PaymentRecord.DoesNotExist:
#             return Response({"detail": "Payment not found."}, status=status.HTTP_404_NOT_FOUND)

#         is_verified = request.data.get("is_verified")
#         if is_verified is None:
#             return Response({"detail": "is_verified field required."}, status=status.HTTP_400_BAD_REQUEST)

#         payment.is_verified = bool(is_verified)

#         if payment.is_verified:
#             payment.verified_at = timezone.now()
#             payment.verified_by = request.user
#             payment.save(update_fields=["is_verified", "verified_at", "verified_by"])
#             # Create enrollment if it doesn't already exist
#             Enrollment.objects.get_or_create(
#                 student=payment.student,
#                 course=payment.course,
#                 defaults={"is_active": True},
#             )
#             return Response({"detail": "Payment verified. Student enrolled successfully."})
#         else:
#             payment.verified_at = None
#             payment.verified_by = None
#             payment.save(update_fields=["is_verified", "verified_at", "verified_by"])
#             # Revoke enrollment
#             Enrollment.objects.filter(student=payment.student, course=payment.course).delete()
#             return Response({"detail": "Payment unverified. Enrollment revoked."})


# ── Enrollment Cancellation ──────────────────────────────────────────────────

class AdminEnrollmentListView(generics.ListAPIView):
    """GET /api/admin/enrollments/ — all enrollments."""
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        from enrollment.models import Enrollment
        from enrollment.serializers import EnrollmentSerializer
        return Enrollment.objects.select_related("student", "course").order_by("-enrolled_at")

    def list(self, request, *args, **kwargs):
        from enrollment.models import Enrollment
        qs = Enrollment.objects.select_related("student", "course").order_by("-enrolled_at")
        data = [
            {
                "id":            e.id,
                "student_id":    e.student.id,
                "student_name":  e.student.get_full_name() or e.student.username,
                "student_email": e.student.email,
                "course_id":     e.course.id,
                "course_title":  e.course.title,
                "enrolled_at":   e.enrolled_at,
                "is_active":     e.is_active,
            }
            for e in qs
        ]
        return Response(data)


class AdminEnrollmentCancelView(APIView):
    """
    DELETE /api/admin/enrollments/<id>/cancel/
    Admin cancels (removes) a student's enrollment.
    """
    permission_classes = [IsAdminUser]

    def delete(self, request, pk):
        try:
            enrollment = Enrollment.objects.select_related("student", "course").get(pk=pk)
        except Enrollment.DoesNotExist:
            return Response({"detail": "Enrollment not found."}, status=status.HTTP_404_NOT_FOUND)

        student_name  = enrollment.student.get_full_name() or enrollment.student.username
        course_title  = enrollment.course.title

        # Also unverify any associated payment so the payment record reflects reality
        PaymentRecord.objects.filter(
            student=enrollment.student,
            course=enrollment.course,
        ).update(is_verified=False, verified_at=None, verified_by=None)

        enrollment.delete()

        return Response(
            {"detail": f"Enrollment of '{student_name}' in '{course_title}' cancelled."},
            status=status.HTTP_200_OK,
        )