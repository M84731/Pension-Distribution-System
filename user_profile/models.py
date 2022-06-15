from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator


SERVICE_STATUS_CHOCIES = [
    ('ACTIVE' , 'ACTIVE'),
   ( 'RETIREE' , 'RETIREE'),
]
     # user profile

class ExtendedUserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,10}$',
                                 message="Phone number must be entered in the format +919999999999. Up to 10 digits allowed.")
    phone = models.CharField('Phone', validators=[phone_regex], max_length=10,  null=True ,blank=True)
    is_phone_verified = models.BooleanField(default=False)
    otp = models.IntegerField(null=True,blank=True)
    """ user additional details """

    service_status = models.CharField(choices=SERVICE_STATUS_CHOCIES, max_length=20, blank=True, null=True)
    date_of_birth = models.DateField(null=True,blank=True)
    address = models.CharField(max_length=100, null=True,blank=True)
    LGA = models.CharField(max_length=100, null=True,blank=True)
    name_of_next_kln = models.CharField(max_length=100, null=True,blank=True)
    next_of_kln_email = models.EmailField(null=True,blank=True)
    next_of_kln_phone = models.CharField(max_length=10, null=True,blank=True)
    next_of_kln_address = models.CharField(max_length=100, null=True,blank=True)


    def __str__(self):
        return str(self.user.username)