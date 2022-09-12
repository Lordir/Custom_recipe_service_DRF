from rest_framework import permissions


class CheckIsActive(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.is_active)


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.author == request.user
