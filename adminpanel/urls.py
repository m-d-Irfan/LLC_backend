from django.urls import path
from .views import (AdminStatsView,AdminUserListView,AdminUserDeleteView,AdminPendingInstructorListView,
    AdminAllInstructorListView,AdminInstructorApproveView,AdminInstructorRejectView,AdminCourseListView,
    AdminCourseDeleteView,
    # AdminPaymentListView,AdminPaymentVerifyView,
    AdminEnrollmentListView,
    AdminEnrollmentCancelView,
)

app_name = "adminpanel"

urlpatterns = [
    path("stats/",AdminStatsView.as_view(),name="stats"),

    path("users/",AdminUserListView.as_view(), name="user-list"),
    path("users/<int:pk>/delete/",AdminUserDeleteView.as_view(),name="user-delete"),

    path("instructors/",AdminAllInstructorListView.as_view(), name="instructor-list"),
    path("instructors/pending/",  AdminPendingInstructorListView.as_view(),name="instructor-pending"),
    path("instructors/<int:pk>/approve/", AdminInstructorApproveView.as_view(), name="instructor-approve"),
    path("instructors/<int:pk>/reject/",AdminInstructorRejectView.as_view(),name="instructor-reject"),

    path("courses/", AdminCourseListView.as_view(),name="course-list"),
    path("courses/<int:pk>/delete/",AdminCourseDeleteView.as_view(), name="course-delete"),

    # path("payments/", AdminPaymentListView.as_view(), name="payment-list"),
    # path("payments/<int:pk>/verify/",  AdminPaymentVerifyView.as_view(),name="payment-verify"),
 
    path("enrollments/",AdminEnrollmentListView.as_view(),name="enrollment-list"),
    path("enrollments/<int:pk>/cancel/",AdminEnrollmentCancelView.as_view(),name="enrollment-cancel"),
]