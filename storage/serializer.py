from rest_framework import serializers
from .models import *


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['id', 'name', 'file_content']


class FolderSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    files = FileSerializer(many=True)

    class Meta:
        model = Folder
        fields = ['id', 'name', 'files']
