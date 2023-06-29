from rest_framework import serializers
from .models import *


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['id', 'name', 'file_content']


class FolderSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    files = FileSerializer(many=True, read_only=True)

    class Meta:
        model = Folder
        fields = ['id', 'name', 'files']


class AddFileInFolderSerializer(serializers.ModelSerializer):
    def save(self, **kwargs):
        folder_id = self.context['folder_id']
        # file_id = self.validated_data['id']
        name = self.validated_data['name']
        file_content = self.validated_data['file_content']
        try:
            file_item = File.objects.get(folder_id=folder_id)
            file_item.save()
            self.instance = file_item
        except File.DoesNotExist:
            self.instance = File.objects.create(
                folder_id=folder_id, **self.validated_data)
        return self.instance

    class Meta:
        model = File
        fields = ['id', 'name', 'file_content']
