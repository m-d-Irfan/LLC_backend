from django.urls import path
from .views import CourseCreateView, CourseListView, CourseDetailView, ModuleCreateView, LessonCreateView, ModuleDetailView, LessonDetailView

app_name = "course"

urlpatterns = [
    path("",CourseListView.as_view(), name = "course-list"),
    path("create/",CourseCreateView.as_view(), name = "course-create"),
    path("<int:pk>/",CourseDetailView.as_view(), name = "course-detail"),
    path("<int:course_pk>/modules/<int:pk>/",ModuleDetailView.as_view(), name = "course-module_detail"),
    path("<int:course_pk>/modules/<int:module_pk>/lessons/<int:pk>/",LessonDetailView.as_view(), name = "course-lesson_detail"),
    path("<int:course_pk>/modules/create/",ModuleCreateView.as_view(), name = "course-module"),
    path("<int:course_pk>/modules/<int:module_pk>/lessons/create/",LessonCreateView.as_view(), name = "course-lesson"),
    # path("module/<int:module_pk>/lessons/create/", LessonCreateView.as_view(), name="lesson-create-flat"),
]

