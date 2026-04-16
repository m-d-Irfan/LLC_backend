# from turtle import title
# from urllib import request

from rest_framework import serializers
from .models import Course, Module, Lesson

class CourseCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = [
            "title",
            "description"
            ]
    
    def create(self,validated_data):
        request = self.context["request"]
        return Course.objects.create(
            created_by = request.user,
            **validated_data
        )


class CourseListSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField()
    class Meta:
        model = Course
        fields = [
            "id",
            "title",
            "description",
            "created_by",
            "created_at",
        ]
        read_only_fields = ["created_by", "created_at"]

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = [
            "id",
            "title",
            "content",
            "video_url",
            "order",
        ]

class ModuleSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many = True, read_only=True)
    class Meta:
        model = Module
        fields = [
            "id",
            "title",
            "order",
            "lessons",
        ]

class CourseDetailSerializer(serializers.ModelSerializer):
    modules = ModuleSerializer(many = True, read_only=True)
    class Meta:
        model = Course
        fields = [
            "id",
            "title",
            "description",
            "created_by",
            "created_at",
            "modules",
        ]
class ModuleCreateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Module
        fields = [
            "title", "order",
        ]

class LessonCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = [
            "title","content","video_url", "order",
        ]