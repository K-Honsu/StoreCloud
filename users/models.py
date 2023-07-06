from django.db import models
from django.contrib.auth.models import BaseUserManager, PermissionsMixin, AbstractBaseUser


class UserAccountManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, username, password=None):
        if not email:
            raise ValueError('Please enter a valid email address')
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            first_name=first_name,
            username=username,
            last_name=last_name
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, first_name, last_name, username, password=None):
        user = self.create_user(
            email,
            password=password,
            first_name=first_name,
            username=username,
            last_name=last_name
        )

        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user


class UserAccount(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255, unique=True, null=True)
    email = models.EmailField(unique=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    objects = UserAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'username']

    def __str__(self):
        return self.first_name + self.last_name


class OTP(models.Model):
    otp = models.CharField(max_length=6)
    user = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE, related_name='otp')
    created_at = models.DateTimeField(auto_now_add=True)

    def check_otp(self, otp):
        return self.otp == otp

    def __str__(self):
        return f'{self.user} -> {self.otp}'
