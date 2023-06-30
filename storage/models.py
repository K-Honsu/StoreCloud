from .enums import AccessControl
from django.db import models
from django.contrib.auth import get_user_model
import uuid
User = get_user_model()


class Folder(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class File(models.Model):
    folder = models.ForeignKey(
        Folder, on_delete=models.CASCADE, related_name='files')
    name = models.CharField(max_length=255)
    file_content = models.FileField(upload_to='upload')
    created_at = models.DateTimeField(auto_now_add=True)
    access_permission = models.ManyToManyField(User, through='FileAccess')

    def __str__(self):
        return self.name


class FileAccess(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, null=True)
    file = models.ForeignKey(File, on_delete=models.CASCADE)
    email = models.EmailField()
    permission = models.CharField(
        choices=[(ap.value, ap.name) for ap in AccessControl], max_length=100, default=AccessControl.VIEW.value)
    requested_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.email} -> {self.file} -> {self.permission}'


# class SendAccess(models.Model):
#     file = models.ForeignKey(
#         File, on_delete=models.CASCADE, related_name='send_access')
#     email = models.EmailField()
#     permissions = models.CharField(choices=[(
#         ap.value, ap.name) for ap in AccessControl], max_length=100, default=AccessControl.VIEW.value)
#     requested_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f'{self.email} -> {self.file} -> {self.permissions}'
