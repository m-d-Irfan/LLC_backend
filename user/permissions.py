from rest_framework.permissions import BasePermission

class IsInstructor(BasePermission):
    message = "Instructor role required. If you recently registered, your account may be awaiting admin approval."

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.is_instructor
            and request.user.instructor_status == "approved"
        )

class IsStudent(BasePermission):
    message = "Student role required."
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_student)

class IsAdminUser(BasePermission):
    """Only Django staff/superusers can access admin panel endpoints."""
    message = "Admin access required."
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_staff)