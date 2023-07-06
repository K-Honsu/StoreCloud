from .serializer import *
from .models import *
from .permissions import IsAnonymous
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.template.loader import get_template
from django.utils.html import strip_tags
from django.utils.crypto import get_random_string
from django.shortcuts import get_object_or_404
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Content
from allauth.socialaccount.models import SocialAccount, SocialToken
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
User = get_user_model()


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        otp = get_random_string(
            length=6, allowed_chars='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789')
        user = serializer.save()
        otp_instance = OTP.objects.create(otp=otp, user=user)
        user.save()

        subject = 'Welcome to StoreCloud'
        template = get_template('email.html')
        context = {'otp': otp, 'user': user}
        message = strip_tags(template.render(context))

        password = serializer.validated_data['password']
        user = serializer.save()
        user.set_password(password)
        user.save()

        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
        return Response({'status': 'success', 'message': 'User created successfully'}, status=status.HTTP_201_CREATED)


class VerfiyOTP(APIView):
    permission_classes = [IsAnonymous]

    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        otp = serializer.validated_data['otp']

        otp_instance = OTP.objects.filter(user__email=email, otp=otp).first()

        if otp_instance:
            user = otp_instance.user
            user.is_active = True
            user.save()
            subject = 'Welcome to StoreCloud'
            template = get_template('success.html')
            context = {'user': user}
            message = strip_tags(template.render(context))
            send_mail(subject, message,
                      settings.DEFAULT_FROM_EMAIL, [user.email])
            return Response({'status': 'success', 'message': 'OTP validated successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'status': 'error', 'message': 'Error validating OTP code'}, status=status.HTTP_400_BAD_REQUEST)

# google oauth
class GoogleOauth(APIView):
    def post(self, request):
        social_account = get_object_or_404(
            SocialAccount,
            user=request.user,
            provider='google'
        )
        access_token = SocialToken.objects.get(
            app__provider='google',
            account=social_account
        ).token
        refresh_token = SocialToken.objects.get(
            app__provider='google',
            account=social_account
        ).token_secret

        username = social_account.extra_data['name']
        first_name = social_account.extra_data['given_name']
        email = social_account.extra_data['email']

        data = {
            'username': username,
            'first_name': first_name,
            'email': email,
            'access_token': access_token,
            'refresh_token': refresh_token,
        }
        print("Access Token:", access_token)
        print("Refresh Token:", refresh_token)
        print(data)

        return Response(data)
