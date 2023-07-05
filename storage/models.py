from .enums import AccessControl
from django.db import models
from django.contrib.auth import get_user_model
import uuid
User = get_user_model()


class Folder(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class File(models.Model):
    folder = models.ForeignKey(
        Folder, on_delete=models.CASCADE, related_name='files')
    name = models.CharField(max_length=255)
    file_url = models.FileField()
    created_at = models.DateTimeField(auto_now_add=True)
    size = models.FloatField(default=0)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.name


class SendAccess(models.Model):
    file = models.ForeignKey(
        File, on_delete=models.CASCADE, related_name='send_access', null=True)
    email = models.EmailField()
    permissions = models.CharField(choices=[(
        ap.value, ap.name) for ap in AccessControl], max_length=100, default=AccessControl.VIEW.value)
    requested_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f'{self.email} -> {self.file} -> {self.permissions}'
