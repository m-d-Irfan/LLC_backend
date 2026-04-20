from django.shortcuts import render
from rest_framework import generics, permissions
from .models import Course, Module, Lesson
from .serializers import CourseCreateSerializer, CourseListSerializer, CourseDetailSerializer, ModuleCreateSerializer, LessonCreateSerializer, ModuleSerializer, LessonSerializer, CourseEnrolledDetailSerializer
from .permissions import IsInstructor
from enrollment.models import Enrollment

class CourseCreateView(generics.CreateAPIView):
    permission_classes = [IsInstructor]
    serializer_class = CourseCreateSerializer

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx["request"] = self.request
        return ctx

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
            is_enrolled = Enrollment.objects.filter(
                student=user,
                course_id=course_pk,
                is_active=True
            ).exists()
            if is_enrolled:
                return CourseEnrolledDetailSerializer  # full content
        return CourseDetailSerializer                  # preview only

    def get_queryset(self):
        return Course.objects.prefetch_related("modules__lessons")

class ModuleCreateView(generics.CreateAPIView):
    permission_classes = [IsInstructor]      
    serializer_class = ModuleCreateSerializer

    def perform_create(self, serializer):
        serializer.save(course_id=self.kwargs["course_pk"])

class LessonCreateView(generics.CreateAPIView):
    permission_classes = [IsInstructor]
    serializer_class = LessonCreateSerializer

    def perform_create(self, serializer):
        serializer.save(module_id=self.kwargs["module_pk"]) 

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
