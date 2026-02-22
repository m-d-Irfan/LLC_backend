from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser

from .serializers import RegisterSerializer, MeSerializer

class HealthView(APIView):
    permission_classes = [permissions.AllowAny]
    def get(self,request):
        return Response({"status":"ok"})

class RegisterView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer

class MeView(generics.RetrieveAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = MeSerializer
    def get_object(self):
        return self.request.user

class ProfileImageUploadView(APIView):
    """
    Allows logged-in user to upload/replace profile image.
    Frontend sends multipart/form-data with key: profile_image
    """
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def patch(self, request):
        user = request.user
        img = request.FILES.get("profile_image")
        if not img:
            return Response({"detail": "profile_image file is required."}, status=400)

        user.profile_image = img
        user.save()
        return Response(MeSerializer(user).data)

