from rest_framework.permissions import BasePermission

class IsStudent(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        else:
            return request.user.is_student

class IsInstructor(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        else:
            return request.user.is_instructor