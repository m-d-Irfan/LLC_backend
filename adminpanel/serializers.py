from django.contrib.auth import get_user_model
from rest_framework import serializers
from course.models import Course

User = get_user_model()


class AdminUserSerializer(serializers.ModelSerializer):
    """Full user record for admin panel listing."""
    course_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id", "username", "email", "first_name", "last_name",
            "is_instructor", "is_student", "is_staff",
            "instructor_status", "instructor_rejection_reason",
            "date_joined", "course_count",
        ]

    def get_course_count(self, obj):
        if obj.is_instructor:
            return Course.objects.filter(created_by=obj).count()
        return 0


class InstructorApproveSerializer(serializers.Serializer):
    """Empty body — just a POST to /approve/ is enough."""
    pass


class InstructorRejectSerializer(serializers.Serializer):
    reason = serializers.CharField(
        max_length=500,
        required=False,
        allow_blank=True,
        default="",
        help_text="Optional reason shown to the instructor in the rejection email.",
    )


class AdminCourseSerializer(serializers.ModelSerializer):
    instructor_name = serializers.SerializerMethodField()
    instructor_email = serializers.SerializerMethodField()
    enrollment_count = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = [
            "id", "title", "description", "price", "is_published",
            "created_at", "instructor_name", "instructor_email", "enrollment_count",
        ]

    def get_instructor_name(self, obj):
        return obj.created_by.get_full_name() or obj.created_by.username

    def get_instructor_email(self, obj):
        return obj.created_by.email

    def get_enrollment_count(self, obj):
        return obj.course_enrollments.count()


class AdminStatsSerializer(serializers.Serializer):
    total_users         = serializers.IntegerField()
    total_students      = serializers.IntegerField()
    total_instructors   = serializers.IntegerField()
    pending_instructors = serializers.IntegerField()
    total_courses       = serializers.IntegerField()
    published_courses   = serializers.IntegerField()
    pending_payments    = serializers.IntegerField()
    verified_payments   = serializers.IntegerField()