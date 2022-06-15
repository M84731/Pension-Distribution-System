from django.contrib import admin
from .models import ExtendedUserProfile


# Register your models here.

@admin.register(ExtendedUserProfile)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user','phone','otp']


