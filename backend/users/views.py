import logging
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.permissions import (AllowAny,
                                        IsAuthenticated,
                                        )

from baselayer.baseapiviews import BaseAPIView
from baselayer.baseauthentication import JWTAuthentication
from utils.mock_responses import ResponseMessages
from product_reviewer import settings
from users.models import (
    User,
)
from users.serializers import (
    RegistrationSerializer,
)
from utils.baseutils import (
    get_first_error_message_from_serializer_errors,
)

logger = logging.getLogger(settings.LOGGER_NAME_PREFIX + __name__)

try:
    from django.contrib.auth.hashers import make_password
    from users.models import User, UserTypeChoices
    User.objects.update_or_create(
        email="superadmin@gmail.com",
        username="superadmin",
        defaults={
            "user_type": UserTypeChoices.ADMIN,
            "password": make_password("helloworld")
        }
    )
except Exception as err:
    print("Error while creating superadmin", err)


class RegistrationView(BaseAPIView):
    """User registration APIView"""

    permission_classes = [AllowAny]
    serializer_class = RegistrationSerializer
    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        """Register a new user.

        Example:
            Request Body:
                API URL: http://baseurl/users/registration/
                {
                    "first_name": "Shakeel",
                    "last_name": "Hassan",
                    "email": "shakeel@domin.com",
                    "password": "pass@word",
                    "location": "Islamabad",
                }

            Response Body:
                {
                    "success": true,
                    "payload": {},
                    "message": "OTP sent successfully."
                }

        """
        print(request)
        serializer_registration = self.serializer_class(data=request.data)
        if not serializer_registration.is_valid():
            logger.error(serializer_registration.errors)
            return self.send_bad_request_response(
                message=get_first_error_message_from_serializer_errors(
                    serialized_errors=serializer_registration.errors,
                    default_message=ResponseMessages.SOMETHING_MISSING_IN_REQUEST,
                )
            )
        user = serializer_registration.save()
        print(user)
        return self.send_success_response(
            payload=self.serializer_class(user).data,
            message=ResponseMessages.ACCOUNT_CREATED
        )


class SignInView(BaseAPIView):
    """User Sign in APIView
    """

    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        # User.objects.filter(phone_number="+923420202688").delete()
        """Login end user

        Example:
            Request Body:
                API URL: http://users/sign-in/
                {
                    "email": "abc@gmail.com",
                    "password": "pass@word"
                }
            Response Body:
                {
                    "success": true,
                    "payload": {
                        "token": "jwt-token"
                    },
                    "message": "Logged in successfully."
                }
        """

        username = request.data.get("username", None)
        password = request.data.get("password", None)

        if not username:
            return self.send_bad_request_response(
                message=ResponseMessages.SOMETHING_MISSING_IN_REQUEST
            )

        if not password:
            return self.send_bad_request_response(
                message=ResponseMessages.SOMETHING_MISSING_IN_REQUEST
            )


        user = User.objects.filter(username=request.data.get("username")).first()
        if not user:
            user = User.objects.filter(email=request.data.get("username")).first()

        if not user:
            return self.send_response(
                success=False,
                message=ResponseMessages.INVALID_EMAIL,
                status_code=status.HTTP_401_UNAUTHORIZED,
            )
        if not user.check_password(request.data.get("password")):
            return self.send_response(
                success=False,
                message=ResponseMessages.INVALID_PASSWORD,
                status_code=status.HTTP_401_UNAUTHORIZED,
            )

        token = user.get_access_token()
        return self.send_success_response(
            message=ResponseMessages.LOGGED_IN_SUCCESSFULLY, payload={"token": token,
                                                                      "username": user.username,
                                                                      "email": user.email,
                                                                      "user_type": user.user_type
                                                                      })
