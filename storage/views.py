from rest_framework.viewsets import ModelViewSet, GenericViewSet
from .models import *
from .serializer import *


class FolderViewSet(ModelViewSet):
    queryset = Folder.objects.prefetch_related('files').all()
    serializer_class = FolderSerializer


class FileViewSet(ModelViewSet):
    # queryset = File.objects.all()
    # serializer_class = FileSerializer

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddFileInFolderSerializer
        return FileSerializer

    def get_serializer_context(self):
        return {'folder_id': self.kwargs['folder_pk']}

    def get_queryset(self):
        return File.objects.filter(folder_id=self.kwargs['folder_pk'])
