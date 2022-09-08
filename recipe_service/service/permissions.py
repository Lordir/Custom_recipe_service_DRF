from rest_framework import permissions


class CheckIsActive(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.is_active)
