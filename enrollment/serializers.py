from rest_framework import serializers
from .models import Enrollment, LessonProgress
from course.serializers import CourseListSerializer


class EnrollmentSerializer(serializers.ModelSerializer):
    course = CourseListSerializer(read_only=True)

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


class LessonProgressSerializer(serializers.ModelSerializer):
    # Return lesson as plain integer so frontend can do p.lesson === lessonId
    lesson = serializers.PrimaryKeyRelatedField(read_only=True)
    # A LessonProgress record existing means the lesson is completed
    completed = serializers.SerializerMethodField()

    def get_completed(self, obj):
        return True

    class Meta:
        model = LessonProgress
        fields = ["id", "lesson", "completed", "completed_at"]
        read_only_fields = ["completed_at"]


class LessonProgressCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonProgress
        fields = ["lesson"]

    def validate_lesson(self, lesson):
        student = self.context["request"].user
        if LessonProgress.objects.filter(student=student, lesson=lesson).exists():
            raise serializers.ValidationError("Lesson already marked as complete.")
        return lesson