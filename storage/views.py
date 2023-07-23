from .permissions import *
from .pagination import DefaultPagination
from .models import *
from .serializer import *
from django.urls import reverse
from django.conf import settings
from django.utils.html import strip_tags
from django.core.mail import send_mail
from django.template.loader import get_template
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.views import APIView
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated


class FolderViewSet(ModelViewSet):
    serializer_class = FolderSerializer
    filter_backends = [SearchFilter]
    search_fields = ['name']

    def get_queryset(self):
        return Folder.objects.filter(user=self.request.user).prefetch_related('files').all()


class FileViewSet(ModelViewSet):
    filter_backends = [SearchFilter]
    search_fields = ['name']
    permission_classes = [FilePermission]
    pagination_class = DefaultPagination

    def get_queryset(self):
        return File.objects.filter(folder_id=self.kwargs['folder_pk'], user=self.request.user).order_by('-created_at')

    def get_serializer_context(self):
        return {'folder_id': self.kwargs['folder_pk']}

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddFileInFolderSerializer
        return FileSerializer


class SendAccessViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_queryset(self):
        return SendAccess.objects.filter(file_id=self.kwargs['file_pk'])

    def get_serializer_context(self):
        return {'file_id': self.kwargs['file_pk']}

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return NewSendAccessSerializer
        elif self.request.method == 'PATCH':
            return UpdateSendAccessSerializer
        return SendAccessSerializer


class RequestAccessView(APIView):
    # def post(self, request, file_pk):
    #     # Get the file object
    #     try:
    #         file = File.objects.get(id=file_pk)
    #     except File.DoesNotExist:
    #         return Response("File not found.", status=status.HTTP_404_NOT_FOUND)
    def post(self, request, folder_pk, file_pk):
        # Retrieve the file object using folder_pk and file_pk
        try:
            file = File.objects.get(folder__id=folder_pk, id=file_pk)
        except File.DoesNotExist:
            return Response({'error': 'File not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Get the user object
        user = request.user

        # Get the file owner
        file_owner = file.user

        # get the file name
        file_name = file.name

        # Get owner email
        owner_email = file_owner.email

        # Generate accept and decline URLs
        accept_url = request.build_absolute_uri(
            reverse('accept_edit_access', args=[file_pk]))
        # decline_url = request.build_absolute_uri(
        #     reverse('decline_edit_access', args=[file_pk]))

        subject = f'Edit Request Access for {file.name}'
        template = get_template('request_access.html')
        context = {'user': user, 'file': file_name,
                   'accept_url': accept_url}  # 'decline_url': decline_url}
        message = strip_tags(template.render(context))
        from_email = settings.DEFAULT_FROM_EMAIL

        send_mail(subject, message, from_email, [owner_email])

        return Response("Request access sent successfully.", status=status.HTTP_200_OK)


def accept_edit_access(request, file_pk):
    # Retrieve the file object based on the file_pk parameter
    try:
        file = File.objects.get(pk=file_pk)
    except File.DoesNotExist:
        return Response({'message': 'File not found'}, status=status.HTTP_404_NOT_FOUND)

    # get the user object
    user = request.user
    # update the user permission
    user.permission = 'edit'
    user.save()
    return Response({'message': 'Edit access granted'}, status=status.HTTP_200_OK)


# request edit access -- done
# google sign in -- done
# storage capacity -- under development
# payment intergration -- under development