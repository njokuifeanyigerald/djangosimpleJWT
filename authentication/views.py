from multiprocessing import AuthenticationError
from django.urls import reverse
from rest_framework import generics, views, response, status, permissions
from .models import User
from .serializer import (EmailVerificationSerializer, LoginSerializer, LogoutSerializer, GoogleSocialAuthSerializer,
         RegisterSerializer, RequestPasswordEmailSerializer,SetNewPasswordSerializer)
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.sites.shortcuts import get_current_site
import jwt
from django.conf import settings
from django.contrib.auth import authenticate
from django.core.mail import send_mail

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .renderers import userRenderer

from .utils import Util

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode


 
from django.contrib import auth



class RegisterAPIView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]
    renderer_classes = [userRenderer]
    def post(self, request, format=None):
        form_data = request.data
        serializer  = self.serializer_class(data=form_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data

        user = User.objects.get(email=user_data['email'])
        token = RefreshToken.for_user(user).access_token


        current_site = get_current_site(request).domain
        relativeLink = reverse('email_verify')

        absurl = 'http://'+current_site+relativeLink+"?token="+str(token)
        email_body = 'Hi '+user.username + \
            ' Use the link below to verify your email \n' + absurl


        data = {'email_body': email_body, 'to_email': user.email,
                'email_subject': 'Verify your email'}

        Util.send_email(data)


        
        return response.Response(user_data, status=status.HTTP_201_CREATED)
        
 
class VerifyEmail(views.APIView):
    serializer_class = EmailVerificationSerializer
    permission_classes = [permissions.AllowAny]
    token_param_config = openapi.Parameter(
        'token', in_=openapi.IN_QUERY, description='use link for email activation', type = openapi.TYPE_STRING
        )
    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY )
            user = User.objects.get(id=payload['user_id'])
            if not user.email_verified:
                user.email_verified = True
                user.save()
                return response.Response({'email': 'account has been successfully activated'},status=status.HTTP_201_CREATED)

            return response.Response({'email': 'account has already been successfully activated'},status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError:
            # just  incase the user didn't activate his/her mail before it expires
            # delete user so user can 
            # user = User.objects.filter(id=payload['user_id'], email_verified=False)
            # user.delete()
            # user.save()
            return response.Response({'error': 'activation link has expired'}, status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError:
            return response.Response({'error': 'invalid token'}, status.HTTP_400_BAD_REQUEST)


class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]
    def post(self, request, format=None):
        data = request.data
        email = data['email']
        password = data['password']

        user = authenticate(email=email, password=password)
        if not user:
            raise AuthenticationError('Invalid credentials, try again')
        if not user.is_active:
            raise AuthenticationError('Account disabled, contact admin')
        if not user.email_verified:
            raise AuthenticationError('Email is not verified')
        if user:
            serializer = self.serializer_class(user)
            # 201 created, because it will create a refresh token and access token
            return response.Response(serializer.data, status=status.HTTP_200_OK)
        return response.Response({'error': 'credentials are not valid'}, status=status.HTTP_401_UNAUTHORIZED)
        

class RequestPasswordResetEmail(generics.GenericAPIView):
    serializer_class = RequestPasswordEmailSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        email = request.data.get('email', '')

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            current_site = get_current_site(request=request).domain
            relativeLink = reverse('password-reset-confirm', kwargs={'uidb64': uidb64, 'token': token})
            redirect_url = request.data.get('redirect_url', '')

            absurl = 'http://'+current_site + relativeLink
            email_body = 'Hello, \n Use link below to reset your password  \n' + \
                absurl+"?redirect_url="+redirect_url
            data = {'email_body': email_body, 'to_email': user.email,
                    'email_subject': 'Reset your passsword'}
            Util.send_email(data)
            return response.Response({'success': 'We have sent you a link to reset your password'}, status=status.HTTP_200_OK)
        return response.Response({'error': 'email does not exist in the database'}, status=status.HTTP_404_NOT_FOUND)


class PasswordTokenCheckAPI(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def get(self, request, uidb64, token):
        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                return response.Response({'error':'token is not valid, please request a new one'})

        except DjangoUnicodeDecodeError as identifier:
            try:
                if not PasswordResetTokenGenerator().check_token(user):
                    return  response.Response({'error': 'token has expired, request a new one'}, status=status.HTTP_400_BAD_REQUEST)
                    
            except UnboundLocalError as e:
                return response.Response({'error': 'Token is not valid, please request a new one'}, status=status.HTTP_400_BAD_REQUEST)


class SetNewPasswordAPIView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return response.Response({'success': True, 'message': 'Password reset success'}, status=status.HTTP_200_OK)


class LogoutView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response({'success': 'successfully logged out'}, status=status.HTTP_204_NO_CONTENT)
  


class GoogleSocialAuthView(generics.GenericAPIView):

    serializer_class = GoogleSocialAuthSerializer

    def post(self, request):
        """
        POST with "auth_token"
        Send an idtoken as from google to get user information
        """

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = ((serializer.validated_data)['auth_token'])
        return response.Response(data, status=status.HTTP_200_OK)
