from rest_framework.permissions import BasePermission
from django.contrib.auth.models import AnonymousUser


class IsAnonymous(BasePermission):
    """ Allows access only to anonymous users. """

    def has_permission(self, request, view):
        return isinstance(request.user, AnonymousUser)
