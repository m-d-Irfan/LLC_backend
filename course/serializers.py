from rest_framework import serializers
from .models import Course, Module, Lesson


class CourseCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ["id", "title", "description", "thumbnail", "price", "is_published"]
        read_only_fields = ["id"]

    def create(self, validated_data):
        request = self.context["request"]
        return Course.objects.create(created_by=request.user, **validated_data)


class CourseUpdateSerializer(serializers.ModelSerializer):
    """Used for PATCH — every field is optional, thumbnail can be cleared."""
    class Meta:
        model = Course
        fields = ["title", "description", "thumbnail", "price", "is_published"]
        extra_kwargs = {
            "title":        {"required": False},
            "description":  {"required": False},
            "price":        {"required": False},
            "is_published": {"required": False},
            "thumbnail":    {"required": False, "allow_null": True},
        }


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ["id", "title", "content", "video_url", "order"]


class ModuleSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Module
        fields = ["id", "title", "order", "lessons"]


class CourseListSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField()
    modules    = ModuleSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = [
            "id", "title", "description",
            "thumbnail", "price", "is_published",
            "created_by", "created_at",
            "modules",
        ]
        read_only_fields = ["created_by", "created_at"]


class LessonPreviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ["id", "title", "order", "video_url"]


class ModulePreviewSerializer(serializers.ModelSerializer):
    lessons = LessonPreviewSerializer(many=True, read_only=True)

    class Meta:
        model = Module
        fields = ["id", "title", "order", "lessons"]


class CourseDetailSerializer(serializers.ModelSerializer):
    modules    = ModulePreviewSerializer(many=True, read_only=True)
    created_by = serializers.StringRelatedField()

    class Meta:
        model = Course
        fields = [
            "id", "title", "description",
            "thumbnail", "price", "is_published",
            "created_by", "created_at",
            "modules",
        ]


class CourseEnrolledDetailSerializer(serializers.ModelSerializer):
    modules    = ModuleSerializer(many=True, read_only=True)
    created_by = serializers.StringRelatedField()

    class Meta:
        model = Course
        fields = [
            "id", "title", "description",
            "thumbnail", "price", "is_published",
            "created_by", "created_at",
            "modules",
        ]


class ModuleCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = ["id", "title", "order"]
        read_only_fields = ["id"]


class ModuleUpdateSerializer(serializers.ModelSerializer):
    """PATCH a module — title and/or order."""
    class Meta:
        model = Module
        fields = ["title", "order"]
        extra_kwargs = {
            "title": {"required": False},
            "order": {"required": False},
        }


class LessonCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ["id", "title", "content", "video_url", "order"]
        read_only_fields = ["id"]


class LessonUpdateSerializer(serializers.ModelSerializer):
    """PATCH a lesson — any combination of fields."""
    class Meta:
        model = Lesson
        fields = ["title", "content", "video_url", "order"]
        extra_kwargs = {
            "title":     {"required": False},
            "content":   {"required": False},
            "video_url": {"required": False, "allow_null": True, "allow_blank": True},
            "order":     {"required": False},
        }