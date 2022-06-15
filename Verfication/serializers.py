from rest_framework import serializers

from Verfication.models import VerificationModel


class VerfificationSerializer(serializers.ModelSerializer):

    class Meta:

        model = VerificationModel
        fields = ('date')