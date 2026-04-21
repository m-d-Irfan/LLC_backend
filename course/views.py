from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Course, Module, Lesson
from .serializers import (
    CourseCreateSerializer, CourseListSerializer, CourseDetailSerializer,
    CourseEnrolledDetailSerializer, CourseUpdateSerializer,
    ModuleCreateSerializer, ModuleUpdateSerializer,
    LessonCreateSerializer, LessonUpdateSerializer,
    ModuleSerializer, LessonSerializer,
)
from .permissions import IsInstructor
from enrollment.models import Enrollment
import cloudinary.uploader


# ── Public / shared ───────────────────────────────────────────────────────

class CourseListView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = CourseListSerializer

    def get_queryset(self):
        return Course.objects.filter(
            is_published=True
        ).select_related("created_by").order_by("-created_at")


class CourseDetailView(generics.RetrieveAPIView):
    permission_classes = [permissions.AllowAny]

    def get_serializer_class(self):
        user = self.request.user
        if user.is_authenticated:
            course_pk = self.kwargs.get("pk")
            try:
                course = Course.objects.get(pk=course_pk)
                if course.created_by == user:
                    return CourseEnrolledDetailSerializer
            except Course.DoesNotExist:
                pass
            is_enrolled = Enrollment.objects.filter(
                student=user, course_id=course_pk, is_active=True
            ).exists()
            if is_enrolled:
                return CourseEnrolledDetailSerializer
        return CourseDetailSerializer

    def get_queryset(self):
        return Course.objects.prefetch_related("modules__lessons").select_related("created_by")


# ── Instructor — course CRUD ───────────────────────────────────────────────

class CourseCreateView(generics.CreateAPIView):
    permission_classes = [IsInstructor]
    serializer_class = CourseCreateSerializer

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx["request"] = self.request
        return ctx


class InstructorCourseListView(generics.ListAPIView):
    """Returns ALL courses (published + draft) owned by the logged-in instructor."""
    permission_classes = [IsInstructor]
    serializer_class = CourseListSerializer

    def get_queryset(self):
        return Course.objects.filter(
            created_by=self.request.user
        ).prefetch_related("modules__lessons").order_by("-created_at")


class CourseUpdateView(generics.UpdateAPIView):
    """PATCH any combination of title/description/price/is_published/thumbnail."""
    permission_classes = [IsInstructor]
    serializer_class = CourseUpdateSerializer
    # http_method_names = ["patch", "options"]

    def get_queryset(self):
        return Course.objects.filter(created_by=self.request.user)


class CourseDeleteView(generics.DestroyAPIView):
    """Delete a course and clean up its Cloudinary thumbnail."""
    permission_classes = [IsInstructor]

    def get_queryset(self):
        return Course.objects.filter(created_by=self.request.user)

    def perform_destroy(self, instance):
        if instance.thumbnail:
            try:
                cloudinary.uploader.destroy(instance.thumbnail.name)
            except Exception:
                pass
        instance.delete()


class CourseRemoveThumbnailView(APIView):
    """POST to wipe the thumbnail from Cloudinary and clear the DB field."""
    permission_classes = [IsInstructor]

    def post(self, request, pk):
        try:
            course = Course.objects.get(pk=pk, created_by=request.user)
        except Course.DoesNotExist:
            return Response({"detail": "Not found."}, status=404)

        if course.thumbnail:
            try:
                cloudinary.uploader.destroy(course.thumbnail.name)
            except Exception:
                pass
            course.thumbnail = None
            course.save()

        return Response({"detail": "Thumbnail removed."})


# ── Modules & Lessons ─────────────────────────────────────────────────────

class ModuleCreateView(generics.CreateAPIView):
    permission_classes = [IsInstructor]
    serializer_class = ModuleCreateSerializer

    def perform_create(self, serializer):
        serializer.save(course_id=self.kwargs["course_pk"])


class ModuleUpdateView(generics.UpdateAPIView):
    """PATCH a module's title and/or order."""
    permission_classes = [IsInstructor]
    serializer_class = ModuleUpdateSerializer
    http_method_names = ["patch"]

    def get_queryset(self):
        # Ensures the instructor owns the parent course
        return Module.objects.filter(course__created_by=self.request.user)


class ModuleDeleteView(generics.DestroyAPIView):
    """Delete a module (cascades to lessons)."""
    permission_classes = [IsInstructor]

    def get_queryset(self):
        return Module.objects.filter(course__created_by=self.request.user)


class LessonCreateView(generics.CreateAPIView):
    permission_classes = [IsInstructor]
    serializer_class = LessonCreateSerializer

    def perform_create(self, serializer):
        serializer.save(module_id=self.kwargs["module_pk"])


class LessonUpdateView(generics.UpdateAPIView):
    """PATCH a lesson's title, content, video_url, and/or order."""
    permission_classes = [IsInstructor]
    serializer_class = LessonUpdateSerializer
    http_method_names = ["patch"]

    def get_queryset(self):
        return Lesson.objects.filter(module__course__created_by=self.request.user)


class LessonDeleteView(generics.DestroyAPIView):
    """Delete a lesson."""
    permission_classes = [IsInstructor]

    def get_queryset(self):
        return Lesson.objects.filter(module__course__created_by=self.request.user)


class ModuleDetailView(generics.RetrieveAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = ModuleSerializer

    def get_queryset(self):
        return Module.objects.prefetch_related("lessons")


class LessonDetailView(generics.RetrieveAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = LessonSerializer

    def get_queryset(self):
        return Lesson.objects.all()