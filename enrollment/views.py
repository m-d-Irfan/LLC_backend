from django.shortcuts import render
from rest_framework import generics, permissions
from .models import Enrollment, LessonProgress
from .serializers import EnrollmentSerializer, EnrollmentCreateSerializer, LessonProgressCreateSerializer, LessonProgressSerializer
from user.permissions import IsStudent

class EnrollmentCreateView(generics.CreateAPIView):
    permission_classes = [IsStudent]
    serializer_class = EnrollmentCreateSerializer
    def perform_create(self, serializer):
        serializer.save(student=self.request.user)

class EnrollmentListView(generics.ListAPIView):
    permission_classes = [IsStudent]
    serializer_class = EnrollmentSerializer

    def get_queryset(self):
        return Enrollment.objects.filter(student = self.request.user)

class LessonProgressCreateView(generics.CreateAPIView):
    permission_classes = [IsStudent]
    serializer_class = LessonProgressCreateSerializer

    def perform_create(self,serializer):
        serializer.save(student = self.request.user)
class LessonProgressListView(generics.ListAPIView):
    permission_classes = [IsStudent]
    serializer_class = LessonProgressSerializer

    def get_queryset(self):
        return LessonProgress.objects.filter(student = self.request.user)
       