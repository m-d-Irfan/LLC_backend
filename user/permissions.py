from rest_framework.permissions import BasePermission

class IsInstructor(BasePermission):
    message = "Instructor role required."
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_instructor)

class IsStudent(BasePermission):
    message = "Student role required."
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_student)