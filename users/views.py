from rest_framework.viewsets import ModelViewSet, GenericViewSet
from django.contrib.auth import get_user_model
from .serializer import *
User = get_user_model()


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        password = serializer.validated_data['password']
        user = serializer.save()
        user.set_password(password)
        user.save()
