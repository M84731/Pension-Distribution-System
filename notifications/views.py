from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from . import serializers, models
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json
from django.contrib.auth.models import User



class NotificationSentView(APIView):
    serializer_class= serializers.NotificationSendSerializer

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
            #     user = self.request.user
            #     notification = serializer.data['notification']
                serializer.save()
                user= serializer.data['user']
                username = User.objects.get(id=user).username
                channel_layer = get_channel_layer()
                notification = serializer.data['notification']
                notification_objs = models.Notification.objects.filter(user_has_seen =False, user= user).count()
                data = {'count':notification_objs,'current_notifications':notification}
                async_to_sync(channel_layer.send)(
                    username,{
                        'type':'send_notification',
                        'value':data
                    }
                )

        except:
            data= serializer.errors
        return Response(data, status=status.HTTP_201_CREATED)


class NotificationRecieveView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        username = request.user.username
        channel_layer = get_channel_layer()
        try:
            notification = async_to_sync(channel_layer.receive)(username)
            print(notification)
        except Exception as e:
            print(e)
        return Response(notification)




