from django.contrib.auth.models import User
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from user_profile.helpers import send_otp_to_phone
from user_profile.models import ExtendedUserProfile
from . import serializers
from rest_framework import status
from .serializers import OtpVerificationSerializer, ResendOtpSerializer,UserProfileSerializer
from rest_framework import status, generics
from rest_framework.response import Response
from .serializers import ForgotPasswordSerializer, RegistrationSerializer, SetNewPasswordSerializer
from rest_framework.generics import GenericAPIView
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import smart_bytes
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.core.mail import send_mail
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
import requests
from django.conf import settings


class RegisterView(GenericAPIView):
    serializer_class = RegistrationSerializer

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            user = serializer.save()
            data['response'] = "An otp has sent to the phone number  and verify  your account "
        else:
            data = serializer.errors
        return Response(data)



class OtpVerificationView(GenericAPIView):
    serializer_class = OtpVerificationSerializer
    def post(self,request):

        serializer = OtpVerificationSerializer(data=request.data)
        data ={}
        if serializer.is_valid():
            user = serializer.save()
            data['response'] = "phone verified ,please login"
        else:
            data = serializer.errors
        return Response(data)


class ForgotPasswordView(APIView):
    serializer_class = serializers.ForgotPasswordSerializer

    def get(self, request):
        serializer = self.serializer_class(data=request.data)
        email= serializer.validated_data['email']

class RequestPasswordResetEmail(generics.GenericAPIView):
    serializer_class = ForgotPasswordSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.data.get('email')
            redirect_url = serializer.data.get('redirect_url')

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            current_site = get_current_site(
                request=request).domain
            relativeLink = reverse('password-token-verify', kwargs={'uidb64': uidb64, 'token': token})
            absurl = 'http://'+current_site + relativeLink
            email_body = 'Hello, \n Use link below to reset your password  \n' + absurl

            send_mail(
                'Pension Distribution System- Reset your password',
                email_body,
                None,
                [user.email],
                fail_silently=False,
            )
        else:
            data = {'response': 'Email does not registerd with us'}
            return Response(data, status=status.HTTP_404_NOT_FOUND)
        return Response({'success': 'We have sent you a link to reset your password'}, status=status.HTTP_200_OK)



class ResetPassword(GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def post(self, request, uidb64, token):
        serializer= self.serializer_class(data=request.data)
        if serializer.is_valid():
                password = serializer.data.get('password')
                try:
                    uid = force_str(urlsafe_base64_decode(uidb64))
                    user = User.objects.get(pk=uid)
                except(TypeError, ValueError, OverflowError, User.DoesNotExist):
                    user = None
                if user is not None and PasswordResetTokenGenerator().check_token(user, token):
                    user.set_password(password)
                    user.save()
                    data = {'response': 'Password reset successfully'}
                else:
                    return Response({'response': 'Link Expired'}, status=status.HTTP_404_NOT_FOUND)
        else:
            data = serializer.errors
        return Response(data, status=status.HTTP_200_OK)
            # return Response({'response': 'valid token'}, status=status.HTTP_200_OK)


class ResendOtp(APIView):
    serializer_class = serializers.ResendOtpSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            phone = serializer.data.get('phone')
            profile = ExtendedUserProfile.objects.get(phone=phone)
            if profile.is_phone_verified == False:

                otp = profile.otp
                email= profile.user.email
                url = f'https://2factor.in/API/V1/{settings.API_KEY}/SMS/{phone}/{otp}'
                response = requests.get(url)
                email_body = 'Hello,\nUse this OTP for completing the verification  \n' + str(otp)
                send_mail(
                    'Pension Distribution System- OTP Verification',
                    email_body,
                    None,
                    [email],
                    fail_silently=False,
                )
                data = {'response': 'OTP Resent'}
            else:
                data = {'response': 'Resent failed'}

        else:
            data = serializer.errors
        return Response(data)


class ServiceStatusView(APIView):
    serializer_class = serializers.ServiceStatusSerializer
    permission_classes = (permissions.IsAuthenticated,)
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            print(request.user)
            status = serializer.data.get('service_status')
            print(status)
            profile = ExtendedUserProfile.objects.get(user=request.user)
            profile.service_status = status
            profile.save()
            data = {'response': 'Service status updated'}
        else:
            data = serializer.errors
        return Response(data)

class UserProfileView(GenericAPIView):
    serializer_class = UserProfileSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        data = {}
        if serializer.is_valid():
            user = ExtendedUserProfile.objects.get(user=request.user)
            print(user.user.username)
            user.date_of_birth = serializer.data.get('date_of_birth')
            user.address = serializer.data.get('address')
            user.LGA = serializer.data.get('LGA')
            user.name_of_next_kln = serializer.data.get('name_of_next_kln ')
            user.next_of_kln_email = serializer.data.get('next_of_kln_email')
            user.next_of_kln_phone = serializer.data.get('next_of_kln_phone')
            user.next_of_kln_address = serializer.data.get('next_of_kln_address')

            user.save()
            data['response'] = "User Profile Updated Successfully "
        else:
            data = serializer.errors
        return Response(data)

    permission_classes = (permissions.IsAuthenticated,)
    def put(self,request):
        user = ExtendedUserProfile.objects.get(user=request.user)
        serializer = UserProfileSerializer(user,data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response (serializer.data)
        return Response({'message':'error','error':serializer.errors})






