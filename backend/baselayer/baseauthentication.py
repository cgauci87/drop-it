import datetime
import jwt

from django.conf import settings
from django.middleware.csrf import CsrfViewMiddleware
from django.views.decorators.csrf import csrf_exempt
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication


class CSRFCheck(CsrfViewMiddleware):
    def _reject(self, request, reason):
        # Return the failure reason instead of an HttpResponse
        return reason


class JWTAuthentication(BaseAuthentication):
    """
        custom authentication class for DRF and JWT
        https://github.com/encode/django-rest-framework/blob/master/rest_framework/authentication.py
    """

    @csrf_exempt
    def authenticate(self, request):

        authorization_header = request.headers.get('Authorization')

        if not authorization_header:
            return None
        try:
            access_token = authorization_header.split(' ')[1]
            payload = jwt.decode(access_token, settings.SECRET_KEY, algorithms=['HS256'])

        except IndexError:
            raise exceptions.AuthenticationFailed('Token prefix missing')
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('Token expired')
        except jwt.InvalidTokenError:
            raise exceptions.NotAcceptable('Invalid token')

        from users.models import User
        user = User.objects.filter(email=payload['email']).first()
        if user is None:
            raise exceptions.AuthenticationFailed('User not found')

        return user, None


class JWTAdminAuthentication(BaseAuthentication):
    """
        custom authentication class for DRF and JWT
        https://github.com/encode/django-rest-framework/blob/master/rest_framework/authentication.py
    """

    @csrf_exempt
    def authenticate(self, request):

        authorization_header = request.headers.get('Authorization')

        if not authorization_header:
            return None
        try:
            access_token = authorization_header.split(' ')[1]
            payload = jwt.decode(access_token, settings.SECRET_KEY, algorithms=['HS256'])

        except IndexError:
            raise exceptions.AuthenticationFailed('Token prefix missing')
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('Token expired')
        except jwt.InvalidTokenError:
            raise exceptions.NotAcceptable('Invalid token')

        from users.models import User, UserTypeChoices
        user = User.objects.filter(email=payload['email'], user_type=UserTypeChoices.ADMIN).first()
        if user is None:
            raise exceptions.AuthenticationFailed('User not found')

        return user, None


class JWTModeratorAuthentication(BaseAuthentication):
    """
        custom authentication class for DRF and JWT
        https://github.com/encode/django-rest-framework/blob/master/rest_framework/authentication.py
    """

    @csrf_exempt
    def authenticate(self, request):

        authorization_header = request.headers.get('Authorization')

        if not authorization_header:
            return None
        try:
            access_token = authorization_header.split(' ')[1]
            payload = jwt.decode(access_token, settings.SECRET_KEY, algorithms=['HS256'])

        except IndexError:
            raise exceptions.AuthenticationFailed('Token prefix missing')
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('Token expired')
        except jwt.InvalidTokenError:
            raise exceptions.NotAcceptable('Invalid token')

        from users.models import User, UserTypeChoices
        user = User.objects.filter(email=payload['email'], user_type=UserTypeChoices.MODIRATOR).first()
        if user is None:
            raise exceptions.AuthenticationFailed('User not found')

        return user, None


def generate_access_token(user):
    access_token_payload = {
        'email': user.email,
        'iat': datetime.datetime.utcnow(),
        'user_type': user.user_type
    }
    encoded_token = jwt.encode(access_token_payload, settings.SECRET_KEY, algorithm='HS256')
    # access_token = encoded_token.decode('utf-8')
    return encoded_token
