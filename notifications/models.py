from django.db import models
from django.contrib.auth.models import User
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json



class Notification(models.Model):

    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    notification = models.TextField(max_length=100)
    user_has_been = models.CharField(default=False,max_length=100)


