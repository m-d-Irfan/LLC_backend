from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from user.views import RegisterView

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView, TokenObtainPairView

urlpatterns = [
    path("admin/", admin.site.urls),

    path("api/auth/", include("dj_rest_auth.urls")),
    path("api/auth/token/", TokenObtainPairView.as_view(), name="jwt-login"),
    path("api/auth/register/",RegisterView.as_view(), name = "register"),

    # Optional: JWT utilities (keep only if you will call them from React)
    path("api/auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/auth/token/verify/", TokenVerifyView.as_view(), name="token_verify"),

    # API docs
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="docs"),

    # Your app APIs
    path("api/user/", include(("user.urls", "user"), namespace="user")),
    path("api/course/", include(("course.urls", "course"), namespace="course")),
    path("api/enrollment/", include(("enrollment.urls", "enrollment"), namespace="enrollment")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
