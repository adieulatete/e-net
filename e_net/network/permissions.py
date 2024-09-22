from rest_framework.permissions import BasePermission


class IsActiveEmployee(BasePermission):
    """Permission class that checks if the user is authenticated and active."""
    def has_permission(self, request, view):
        return (
            request.user and 
            request.user.is_authenticated and 
            request.user.is_active
        )
