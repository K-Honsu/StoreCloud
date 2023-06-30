from rest_framework.viewsets import ModelViewSet, GenericViewSet
from .permissions import *
from .models import *
from .serializer import *
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated


class FolderViewSet(ModelViewSet):
    queryset = Folder.objects.prefetch_related('files').all()
    serializer_class = FolderSerializer


class FileViewSet(ModelViewSet):
    def get_queryset(self):
        return File.objects.filter(folder_id=self.kwargs['folder_pk'])

    def get_serializer_context(self):
        return {'folder_id': self.kwargs['folder_pk']}

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddFileInFolderSerializer
        return FileSerializer


class FileAccessViewSet(ModelViewSet):
    queryset = FileAccess.objects.all()
    # permission_classes = [FilePermission | IsAuthenticated]

    # def get_queryset(self):
    #     queryset = FileAccess.objects.all()
    #     if self.request.user.is_authenticated:
    #         user_email = self.request.user.email
    #     else:
    #         user_permissions = FileAccess.objects.filter(
    #             email=user_email).values_list('permission', flat=True)
    #         allowed_permissions = ['edit', 'comment']

    #         if 'edit' in user_permissions or 'comment' in user_permissions:
    #             queryset = FileAccess.objects.filter(
    #                 permission__in=allowed_permissions)
    #         else:
    #             queryset = FileAccess.objects.none()

    #     return queryset
    # if self.request.method in ['PUT', 'PATCH']:
    #     user_has_privilege = self.check_user_privilege(
    #         self.request.user, self.kwargs['pk'])
    #     if not user_has_privilege:
    #         query = query.none()
    # return query

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return NewFileAccessSerializer
        return FileAccessSerializer

    # def check_user_privilege(self, user, file_access_id):
    #     return FilePermission().check_user_privilege(user, file_access_id)
