from django.shortcuts import render
from rest_framework import generics, permissions
from .models import Course, Module, Lesson
from .serializers import CourseCreateSerializer, CourseListSerializer, CourseDetailSerializer, ModuleCreateSerializer, LessonCreateSerializer, ModuleSerializer, LessonSerializer
from .permissions import IsInstructor

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
        return Course.objects.select_related("created_by").order_by("-created_at")

class CourseDetailView(generics.RetrieveAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = CourseDetailSerializer

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
