from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsSuperUser(BasePermission):
    """Check if user is super user"""
    message = 'You must be superuser'

    def has_permission(self, request, view):
        return bool(
            request.user.is_authenticated and request.user.is_superuser
        )


class IsSuperUserOrReadOnly(BasePermission):
    """Check if user is superuser or read only"""

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return bool(
            request.user.is_authenticated and request.user.is_superuser
        )
