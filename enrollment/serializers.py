from rest_framework import serializers
from .models import Enrollment, LessonProgress
from course.models import Lesson

class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = [
            "id", "course", "enrolled_at", "is_active"

        ]
        read_only_fields = ["enrolled_at","is_active"]

class EnrollmentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = ["course"]

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
        fields = ["id","lesson","completed_at","is_complete"]
        read_only_fields = ["completed_at"]

class LessonProgressCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonProgress
        fields = ["lesson"]



