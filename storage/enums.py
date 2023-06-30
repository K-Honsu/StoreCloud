from django.db.models import TextChoices


class AccessControl(TextChoices):
    EDIT = 'editor'
    VIEW = 'viewer'
    COMMENT = 'commentor'
