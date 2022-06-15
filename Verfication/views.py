from django.shortcuts import render
from rest_framework import generics, serializers, status
from rest_framework.response import Response
from Verfication.models import VerificationModel
from Verfication.serializers import VerfificationSerializer

class BookVerificationView(generics.CreateAPIView):
    serializer_class = VerfificationSerializer
    queryset = VerificationModel.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.request.user
        serializer.save(user=user)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)





