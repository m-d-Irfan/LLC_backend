from django.urls import path
from .views import CourseCreateView, CourseListView

app_name = "course"

urlpatterns = [
    path("",CourseListView.as_view(), name = "list"),
    path("create/",CourseCreateView.as_view(), name = "create")
]

