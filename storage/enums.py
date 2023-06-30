from django.db.models import TextChoices


class AccessControl(TextChoices):
    EDITOR = 'editor'
    VIEWER = 'viewer'
    COMMENTOR = 'commentor'
