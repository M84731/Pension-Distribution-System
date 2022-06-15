from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from . import views
from .views import RegisterView,OtpVerificationView

urlpatterns = [
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('request-passwordreset/', views.RequestPasswordResetEmail.as_view(), name='request-passwordreset'),
    path('password-token-verify/<uidb64>/<token>/', views.ResetPassword.as_view(), name='password-token-verify'),
    path('register/', RegisterView.as_view(), name='register'),
    path('verify-otp/',OtpVerificationView.as_view(),name ="verify-otp"),
    path('resend-otp/',views.ResendOtp.as_view(),name="resend-otp"),
    path('servie_status/',views.ServiceStatusView.as_view(),name="servie_status"),
    path('user-details/',views.UserProfileView.as_view(),name ="user-details"),

]


