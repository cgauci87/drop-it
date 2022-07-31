import logging
from django.conf import settings
from rest_framework.exceptions import ValidationError
from rest_framework.utils.serializer_helpers import ReturnList

logger = logging.getLogger(settings.LOGGER_NAME_PREFIX + __name__)


def get_first_error_message_from_serializer_errors(serialized_errors, default_message=""):
    this_field_is_required = "This field is required."
    if not serialized_errors:
        logger.error(default_message)
        return default_message
    try:
        logger.error(serialized_errors)

        serialized_error_dict = serialized_errors

        # ReturnList of serialized_errors when many=True on serializer
        if isinstance(serialized_errors, ReturnList):
            serialized_error_dict = serialized_errors[0]
        elif isinstance(serialized_errors, ValidationError):
            serialized_error_dict = serialized_errors.detail

        serialized_errors_keys = list(serialized_error_dict.keys())
        # getting first error message from serializer errors
        error_message = serialized_error_dict[serialized_errors_keys[0]][0]
        if error_message == this_field_is_required:
            error_message = error_message.replace("This", serialized_errors_keys[0])
        return error_message
    except Exception as e:
        logger.error(f"Error parsing serializer errors:{e}")
        return default_message
