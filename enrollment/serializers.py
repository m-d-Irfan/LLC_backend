from rest_framework import serializers
from .models import Enrollment, LessonProgress
from course.models import Lesson
from course.serializers import CourseListSerializer 

class EnrollmentSerializer(serializers.ModelSerializer):
    course = CourseListSerializer(read_only=True)  # nest course, not just FK int

    class Meta:
        model = Enrollment
        fields = ["id", "course", "enrolled_at", "is_active"]
        read_only_fields = ["enrolled_at", "is_active"]

class EnrollmentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = ["course"]

    def validate_course(self, course):
        student = self.context["request"].user
        if Enrollment.objects.filter(student=student, course=course).exists():
            raise serializers.ValidationError("You are already enrolled in this course.")
        return course

class LessonSummarySerializer(serializers.ModelSerializer):
    module_title = serializers.CharField(source="module.title")
    course_title = serializers.CharField(source="module.course.title")

    class Meta:
        model = Lesson
        fields = ["id", "title", "module_title", "course_title"]


class LessonProgressSerializer(serializers.ModelSerializer):
    lesson = LessonSummarySerializer(read_only=True)
    class Meta:
        model = LessonProgress
        fields = ["id","lesson","completed_at"]
        read_only_fields = ["completed_at"]

class LessonProgressCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonProgress
        fields = ["lesson"]



