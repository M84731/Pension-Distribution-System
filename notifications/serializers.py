from rest_framework import serializers

from notifications.models import Notification


class NotificationSendSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ('user','notification')