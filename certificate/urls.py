from django.urls import path
from .views import (CertificateListView, FinishCourseView)

app_name = "certificate"

urlpatterns = [
    path("", CertificateListView.as_view(), name = "certificate-list" ),
    path("finish/", FinishCourseView.as_view(), name = "finish-course")
]
