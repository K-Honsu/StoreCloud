from django.db import models
import uuid


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

    def __str__(self):
        return self.name
