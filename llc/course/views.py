from django.shortcuts import render
from rest_framework import generics, permissions
from .models import Course
from .serializers import CourseCreateSerializer, CourseListSerializer

class CourseCreateView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
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




