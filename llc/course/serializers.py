from turtle import title
from urllib import request

from rest_framework import serializers
from .models import Course

class CourseCreateSerializer(serializers.ModelSerializer):
    class meta:
        model = Course
        fields = ["title","description"]
    
    def create(self,validated_data):
        request = self.context["request"]
        return Course.objects.create(
            created_by = request.user,
            **validated_data
        )


class CourseListSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField()
    class meta:
        model = Course
        fields = [
            "id",
            "title",
            "description",
            "created_by",
            "created_at",
        ]
        read_only_fields = ["created_by", "created_at"]

