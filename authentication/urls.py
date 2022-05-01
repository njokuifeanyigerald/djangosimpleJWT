from django.urls import path
from .views import (RegisterAPIView, VerifyEmail,LoginAPIView,LogoutView,GoogleSocialAuthView,
     RequestPasswordResetEmail, PasswordTokenCheckAPI, SetNewPasswordAPIView)

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('google/', GoogleSocialAuthView.as_view(), name="google"),
    path('email_verify/', VerifyEmail.as_view(), name='email_verify'),
    path('request-password-reset/', RequestPasswordResetEmail.as_view(), name='request-password-reset'),
    path('password-reset/<uidb64>/<token>/', PasswordTokenCheckAPI.as_view(), name='password-reset-confirm'),
    path('password-reset-complete', SetNewPasswordAPIView.as_view(),
         name='password-reset-complete')
]
