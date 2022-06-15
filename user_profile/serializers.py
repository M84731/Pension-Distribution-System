from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from .models import ExtendedUserProfile
from rest_framework.response import Response
from .helpers import send_otp_to_phone
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework.exceptions import AuthenticationFailed


""" Creating register serializer"""
class RegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    phone = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2', 'phone')
        extra_kwargs = {
            'password': {'required': True},
        }

    def validate(self, attrs):
        phone = attrs.get('phone')
        if phone is None:
            return Response({
                'status': 400,
                'message': 'key phone_number is required'
            })
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            is_active=False
        )
        userprofile = ExtendedUserProfile.objects.create(

            user=user,
            phone=validated_data['phone'],
            otp=send_otp_to_phone(validated_data['phone'],validated_data['email'])
        )
        user.set_password(validated_data['password'])
        user.save()
        userprofile.save()

        return Response({
            'status': True,
            'user': user,
            'userprofile': userprofile,

        })

""" sending otp verification """

class OtpVerificationSerializer(serializers.ModelSerializer):
    phone = serializers.IntegerField(write_only=True, required=False)
    otp = serializers.IntegerField(write_only=True)

    class Meta:
        model = ExtendedUserProfile
        fields = ('phone', 'otp')

    def validate(self, attrs):
        phone = attrs.get('phone')
        otp = attrs.get('otp')
        if phone is None:
            return Response({
                'status': 400,
                'message': 'key phone number is required'
            })
        if otp is None:
            return Response({
                'status': 400,
                'meassge': 'key otp is required'
            })
        return attrs

    def create(self, validated_data):
        try:
            userprofile = ExtendedUserProfile.objects.get(
                phone=validated_data['phone'])
            if userprofile.is_phone_verified == False:
                print(validated_data['phone'])
                print(userprofile.otp)
                if userprofile.otp == validated_data['otp']:
                    email = userprofile.user.email
                    user = User.objects.get(email=email)
                    if user:
                        user.is_active = True
                        user.save()
                    userprofile.is_phone_verified = True
                    userprofile.save()

                    return Response({
                        'status': 200,
                        'message': 'otp Matched'
                    })
            else:
                raise serializers.ValidationError(
                    "human readable error message here")

        except Exception as e:
            return Response({
                'status': 400,
                'message': 'invalid phone'
            })

""" forgot password"""
class ForgotPasswordSerializer(serializers.Serializer):

    email = serializers.EmailField()
    redirect_url = serializers.CharField(max_length=500, required=False)

    class Meta:
        fields = ['email',]

""" create confirm password"""
class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=6, max_length=68)
    confirm_password = serializers.CharField(min_length=6, max_length=68)

    class Meta:
        fields = ['password','confirm_password']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            confirm_password = attrs.get('confirm_password')
            if password != confirm_password:
                raise serializers.ValidationError(
                    {"password": "Password fields didn't match."})
            else:
                return attrs
        except:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})


class ResendOtpSerializer(serializers.Serializer):
    phone = serializers.IntegerField( required=False)

    class Meta:
        fields = ['phone']



class ServiceStatusSerializer(serializers.Serializer):
    service_status = serializers.ChoiceField(choices=['ACTIVE', 'RETIREE'])

    class Meta:
        fields = ['service_status']



class UserProfileSerializer(serializers.ModelSerializer):


    """ A serializer for our user profile objects"""

    class Meta:
        model = ExtendedUserProfile
        fields = ['date_of_birth','address','LGA','name_of_next_kln','next_of_kln_email','next_of_kln_phone','next_of_kln_address']



