from .serializer import *
from .models import *
from django.conf import settings
from django.contrib.auth import get_user_model
# from django.core.mail import send_mail
from django.template.loader import get_template
from django.utils.html import strip_tags
from django.utils.crypto import get_random_string
from django.shortcuts import get_object_or_404
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Content
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated

from pprint import pprint

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

        mail = Mail(
            from_email=settings.DEFAULT_FROM_EMAIL,
            # to_emails=user.email,
            to_email=user.email,
            # html_content=message,
            subject=subject)

        # mail.add_to(user.email)
        mail.content = Content("text/html", message)

        try:
            sendgrid_client = SendGridAPIClient(
                api_key=settings.SENDGRID_API_KEY)
            response = sendgrid_client.send(mail)
            print(response)
        except Exception as e:
            # Handle the exception here
            print(str(e))
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        response_data = {'id': user.id, 'email': user.email}
        return Response(response_data, status=status.HTTP_201_CREATED)

        # from_email = settings.DEFAULT_FROM_EMAIL
        # receipient_list = [user.email]
        # send_mail(subject, message, from_email, receipient_list)
        # response_data = {'id': user.id, 'email': user.email}
        # return Response(response_data, status=status.HTTP_201_CREATED)


class VerfiyOTP(APIView):
    # permission_classes = [All]

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
            return Response({'status': 'success', 'message': 'OTP validated successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'status': 'error', 'message': 'Error validating OTP code'}, status=status.HTTP_400_BAD_REQUEST)
