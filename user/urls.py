from urllib.parse import urlparse

from django.urls import path
from .views import HealthView, RegisterView, MeView
# from .views import ProfileImageUploadView

urlpatterns = [
    path("health/", HealthView.as_view(), name = "health"),
    # path("auth/register/", RegisterView.as_view(), name = "register"),
    # path("auth/login/", TokenObtainPairView.as_view(), name="jwt-login"),
    # path("auth/refresh/", TokenRefreshView.as_view(), name="jwt-refresh"),
    path("me/", MeView.as_view(), name = "me"),
    # path("profile-image/", ProfileImageUploadView.as_view(), name="profile_image"),

]