from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser

from .serializers import RegisterSerializer, MeSerializer
# from .serializers import  ProfileImageUpdateSerializer


class HealthView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        return Response({"status": "ok"})


class RegisterView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer


class MeView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]   # ✅ FIX
    serializer_class = MeSerializer

    def get_object(self):
        return self.request.user

    def get_serializer_context(self):
        # ✅ ensures profile_image_url can be absolute
        ctx = super().get_serializer_context()
        ctx["request"] = self.request
        return ctx


# class ProfileImageUploadView(APIView):
#     permission_classes = [permissions.IsAuthenticated]
#     parser_classes = [MultiPartParser, FormParser]

#     def patch(self, request):
#         serializer = ProfileImageUpdateSerializer(
#             request.user, data=request.data, partial=True, context={"request": request}
#         )
#         serializer.is_valid(raise_exception=True)
#         serializer.save()

#         # return full "me" payload consistently
#         return Response(
#             MeSerializer(request.user, context={"request": request}).data,
#             status=status.HTTP_200_OK,
#         )