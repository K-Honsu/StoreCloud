from .models import OTP
from rest_framework import serializers
from django.contrib.auth import get_user_model
User = get_user_model()


class UserOtpSerializer(serializers.ModelSerializer):
    class Meta:
        model = OTP
        fields = ['otp', 'user', 'created_at']


class UserSerializer(serializers.ModelSerializer):
    otp = UserOtpSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'password', 'otp']
        ref_name = 'user_account'


# class VerifyOTPSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = OTP
#         fields = ['id', 'otp']
# class VerifyOTPSerializer(serializers.ModelSerializer):
#     otp = serializers.CharField(max_length=6)

#     def validate(self, data):
#         otp = data['otp']
#         user = self.context['request'].user

#         try:
#             otp_instance = OTP.objects.get(user=user)
#         except OTP.DoesNotExist:
#             raise serializers.ValidationError('Invalid OTP')

#         if not otp_instance.check_otp(otp):
#             raise serializers.ValidationError('Invalid OTP')

#         return data

#     class Meta:
#         model = OTP
#         fields = ['otp']

# serializer.py
class VerifyOTPSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)

    class Meta:
        model = OTP
        fields = ['id', 'email', 'otp']
