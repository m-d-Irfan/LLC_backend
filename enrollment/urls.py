from django.urls import path
from .views import EnrollmentCreateView, EnrollmentListView, LessonProgressCreateView, LessonProgressListView, InstructorCourseListView

app_name = "enrollment"

urlpatterns = [
    path("",EnrollmentListView.as_view(), name = "enroll-list"),
    path("mine/", InstructorCourseListView.as_view(), name="course-mine"),
    path("enroll/",EnrollmentCreateView.as_view(), name = "enroll-create"),
    path("progress/",LessonProgressListView.as_view(), name = "progress-list"),
    path("progress/complete/",LessonProgressCreateView.as_view(), name = "progress-complete"),
    
]