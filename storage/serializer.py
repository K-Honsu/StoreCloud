from django.conf import settings
from rest_framework import serializers
from .models import *
import cloudinary
from cloudinary.uploader import upload


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
        fields = ['id', 'name', 'file_url', 'send_access']


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
        file_url = self.validated_data['file_url']

        response = upload(
            file_url, resource_type='auto', api_key=settings.CLOUDINARY_API_KEY, api_secret=settings.CLOUDINARY_API_SECRET, cloud_name=settings.CLOUDINARY_CLOUD_NAME)
        file_url = response['secure_url']

        self.instance = File.objects.create(
            folder_id=folder_id, **self.validated_data)
        return self.instance

    class Meta:
        model = File
        fields = ['id', 'name', 'file_url']
