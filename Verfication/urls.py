from django.urls import path
from . import views

urlpatterns = [
    path('verification/', views.BookVerificationView.as_view(), name='verification'),
]