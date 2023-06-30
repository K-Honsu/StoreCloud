from rest_framework import permissions
from .enums import AccessControl
from .models import FileAccess


class FilePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_file_permission(self, request, view, obj):
        if obj.user == request.user:
            return True
        elif obj.permission == 'edit':
            return True
        elif obj.permission == 'comment':
            return True
        else:
            return False

    # def has_file_permission(self, request, view, obj):
    #     user = request.user
    #     if user == obj.user:
    #         return True

    #     permission = obj.permission
    #     if permission == AccessControl.EDIT.value:
    #         return user in obj.file.can_edit.all()
    #     elif permission == AccessControl.VIEW.value:
    #         return user in obj.file.can_view.all()
    #     elif permission == AccessControl.COMMENT.value:
    #         return user in obj.file.can_comment.all()

    #     return False

    # def check_user_privilege(self, user, file_access_id):
    #     try:
    #         file_access = FileAccess.objects.get(id=file_access_id)
    #     except FileAccess.DoesNotExist:
    #         return False

    #     if user == file_access.user:
    #         return True

    #     permission = file_access.permission
    #     if permission == AccessControl.EDIT.value:
    #         return user in file_access.file.can_edit.all()
    #     elif permission == AccessControl.VIEW.value:
    #         return user in file_access.file.can_view.all()
    #     elif permission == AccessControl.COMMENT.value:
    #         return user in file_access.file.can_comment.all()

    #     return False
