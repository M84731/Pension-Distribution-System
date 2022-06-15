import random
import requests
from django.conf import settings
from django.core.mail import send_mail


def send_otp_to_phone(phone,email):
    try:
        otp = random.randint(1000,9999)
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
        return otp
    except Exception as e:
        return None