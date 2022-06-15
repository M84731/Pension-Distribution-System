from django.urls import path

from . import views

urlpatterns = [
    path('notification/', views.NotificationSentView.as_view(), name='notification_sent'),
    path('notification_recieve/', views.NotificationRecieveView.as_view(), name='notification_recieve'),

]