from urllib.parse import urlparse

from django.urls import path
from .views import HealthView, RegisterView, MeView, ProfileImageUploadView

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
app_name = "user"
urlpatterns = [
    path("health/", HealthView.as_view(), name = "health"),
    path("auth/register/", RegisterView.as_view(), name = "register"),
    path("auth/login/", TokenObtainPairView.as_view(), name="jwt-login"),
    path("auth/refresh/", TokenRefreshView.as_view(), name="jwt-refresh"),
    path("auth/me/", MeView.as_view(), name = "me"),
    path("profile-image/", ProfileImageUploadView.as_view(), name="profile-image"),

]