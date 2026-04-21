from django.urls import path
from .views import (
    CourseCreateView, CourseListView, CourseDetailView,
    CourseUpdateView, CourseDeleteView, CourseRemoveThumbnailView,
    InstructorCourseListView,
    ModuleCreateView, ModuleUpdateView, ModuleDeleteView,
    LessonCreateView, LessonUpdateView, LessonDeleteView,
    ModuleDetailView, LessonDetailView,
)

app_name = "course"

urlpatterns = [
    # Public
    path("",                        CourseListView.as_view(),           name="course-list"),
    path("<int:pk>/",               CourseDetailView.as_view(),         name="course-detail"),

    # Instructor — course management
    path("create/",                 CourseCreateView.as_view(),         name="course-create"),
    path("mine/",                   InstructorCourseListView.as_view(), name="course-mine"),
    path("<int:pk>/update/",        CourseUpdateView.as_view(),         name="course-update"),
    path("<int:pk>/delete/",        CourseDeleteView.as_view(),         name="course-delete"),
    path("<int:pk>/remove-thumbnail/", CourseRemoveThumbnailView.as_view(), name="course-remove-thumbnail"),

    # Modules — create (nested under course), update/delete (flat by pk)
    path("<int:course_pk>/modules/create/",
         ModuleCreateView.as_view(),  name="course-module-create"),
    path("module/<int:pk>/update/",
         ModuleUpdateView.as_view(),  name="course-module-update"),
    path("module/<int:pk>/delete/",
         ModuleDeleteView.as_view(),  name="course-module-delete"),

    # Lessons — create (nested), update/delete (flat by pk)
    path("<int:course_pk>/modules/<int:module_pk>/lessons/create/",
         LessonCreateView.as_view(),  name="course-lesson-create"),
    path("lesson/<int:pk>/update/",
         LessonUpdateView.as_view(),  name="course-lesson-update"),
    path("lesson/<int:pk>/delete/",
         LessonDeleteView.as_view(),  name="course-lesson-delete"),

    # Detail (read-only, public)
    path("<int:course_pk>/modules/<int:pk>/",
         ModuleDetailView.as_view(),  name="course-module-detail"),
    path("<int:course_pk>/modules/<int:module_pk>/lessons/<int:pk>/",
         LessonDetailView.as_view(),  name="course-lesson-detail"),
]