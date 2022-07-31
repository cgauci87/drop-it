"""All views will extend this BaseAPIView View."""

import logging

from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.status import is_server_error
from rest_framework.views import APIView, exception_handler

logger = logging.getLogger(settings.LOGGER_NAME_PREFIX + __name__)


class BaseAPIView(APIView):
    """Base class for API views."""

    @staticmethod
    def make_response_body(success=True,
                           payload=None,
                           message="",
                           ):

        """Make standard response body
        :param success
        :param payload
        :param message
        :return : dictionary including all above params
        """
        return {
            "success": success,
            "payload": {} if payload is None else payload,
            "message": message,
        }

    def send_response(
            self,
            success=True,
            status_code=status.HTTP_200_OK,
            payload=None,
            message="",
            **kwargs,
    ):
        """
        Generates response.
        :param success: bool tells if call is successful or not.
        :param status_code: int HTTP status code.
        :param payload:dict  data generated for respective API call.
        :param message: str message.
        :rtype: dict.
        """
        if not success and is_server_error(status_code):
            if settings.DEBUG:
                message = f"error message: {message}"
            else:
                message = "Internal server error."
        return Response(data=self.make_response_body(success, payload, message),
                        status=status_code,
                        **kwargs
                        )

    def send_success_response(self, message, payload=None, **kwargs):
        """compose success response"""
        return self.send_response(
            status_code=status.HTTP_200_OK,
            payload=payload,
            message=message,
            **kwargs,
        )

    def send_created_response(self, message, payload=None, **kwargs):
        """compose response for new object creation."""
        return self.send_response(
            status_code=status.HTTP_201_CREATED,
            payload=payload,
            message=message,
            **kwargs,
        )

    def send_bad_request_response(self, message):
        """compose response for bad request"""
        return self.send_response(
            success=False,
            status_code=status.HTTP_400_BAD_REQUEST,
            message=message,
        )

    def successful_call(self, response):
        return response.status_code == status.HTTP_200_OK

    def set_render(self, response, request):
        if isinstance(response, Response):
            if not getattr(request, 'accepted_renderer', None):
                neg = self.perform_content_negotiation(request, force=True)
                request.accepted_renderer, request.accepted_media_type = neg

        response.accepted_renderer = request.accepted_renderer
        response.accepted_media_type = request.accepted_media_type
        response.renderer_context = self.get_renderer_context()
        return response


def custom_exception_handler(exc, context):
    """Call REST framework's default exception handler to set a standard error response on error."""
    logger.info("inside of custom exception handler.")

    response = exception_handler(exc, context)
    logger.info(f" context: {context}")
    logger.error(f" exception: {exc}")
    logger.error(f" response: {response}")

    # The exception handler function should either return a Response object,or None
    # If the handler returns None then the exception will be re-raised and
    # Django will return a standard HTTP 500 'server error' response.
    # so override the response None and return standard response with HTTP_400_BAD_REQUEST
    if response is None:
        print(exc)
        return Response(
            data={
                "success": False,
                "payload": {},
                "message": "Something went wrong during process.Try again later.",
            },
            status=status.HTTP_400_BAD_REQUEST,
        )
    return Response(
        data={
            "success": False,
            "payload": {},
            "message": response.data['detail'],
        },
        status=response.status_code,
    )
