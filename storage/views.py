from rest_framework.viewsets import ModelViewSet, GenericViewSet
from .models import *
from .serializer import *


class FolderViewSet(ModelViewSet):
    queryset = Folder.objects.all()
    serializer_class = FolderSerializer


class FileViewSet(ModelViewSet):
    queryset = File.objects.all()
    serializer_class = FileSerializer
