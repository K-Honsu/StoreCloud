from rest_framework import permissions
from .enums import AccessControl


class FilePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_file_permission(self, request, view, obj):
        user = request.user

        if user.access_control == AccessControl.EDIT:
            return True
        elif user.access_control == AccessControl.VIEW:
            return request.method in ['GET', 'HEAD', 'OPTIONS']
        return False
