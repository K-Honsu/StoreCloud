from rest_framework import serializers
from .models import *


class NewSendAccessSerializer(serializers.ModelSerializer):
    def save(self, **kwargs):
        file_id = self.context['file_id']
        email = self.validated_data['email']
        permissions = self.validated_data['permissions']
        self.instance = SendAccess.objects.create(
            file_id=file_id, **self.validated_data)
        return self.instance

    class Meta:
        model = SendAccess
        fields = ['id', 'email', 'permissions']


class UpdateSendAccessSerializer(serializers.ModelSerializer):
    class Meta:
        model = SendAccess
        fields = ['id', 'email', 'permissions']


class FileSerializer(serializers.ModelSerializer):
    send_access = NewSendAccessSerializer(many=True, read_only=True)

    class Meta:
        model = File
        fields = ['id', 'name', 'file_content', 'send_access']


class SendAccessSerializer(serializers.ModelSerializer):
    class Meta:
        model = SendAccess
        fields = ['id',  'email', 'permissions']


class FolderSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    files = FileSerializer(many=True, read_only=True)

    class Meta:
        model = Folder
        fields = ['id', 'name', 'files']


class AddFileInFolderSerializer(serializers.ModelSerializer):
    def save(self, **kwargs):
        folder_id = self.context['folder_id']
        name = self.validated_data['name']
        file_content = self.validated_data['file_content']

        self.instance = File.objects.create(
            folder_id=folder_id, **self.validated_data)
        return self.instance

    class Meta:
        model = File
        fields = ['id', 'name', 'file_content']
