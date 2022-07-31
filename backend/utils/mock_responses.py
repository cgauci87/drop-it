from enum import Enum


class ResponseMessages(str, Enum):
    # User registration messages
    PRODUCT_REVIEW_CREATED_SUCCESSFULLY = "Product review created successfully."
    PRODUCT_ID_AND_APPROVAL_STATUS_IS_REQUIRED = "Product id and approval status is required."
    PRODUCT_DELETED_SUCCESSFULLY = "Product deleted successfully."
    PRODUCT_UPDATED_SUCCESSFULLY = "Product updated successfully."
    PRODUCT_NOT_FOUND = "Product not found"
    PRODUCT_ID_REQUIRED = "Product id is required."
    PRODUCT_CREATED_SUCCESSFULLY = "Product created successfully."
    SOMETHING_MISSING_IN_REQUEST = "Something is missing in request body."
    ACCOUNT_CREATED = "Account created successfully."
    INVALID_EMAIL = "Invalid email"
    INVALID_PASSWORD = "Invalid Password"
    LOGGED_IN_SUCCESSFULLY = "Logged in successfully."
    SOMETHING_MISSING_IN_FORGET_PASSWORD_REQUEST = (
        "Something is missing in forget password request body."
    )
    EMAIL_OTP_SENT = "OTP has been sent succesfuly sent."
    INVALID_OTP_OR_EXPIRED = "Invalid OTP or expired."
    SOMETHING_MISSING_IN_VERIFY_PASSWORD_REQUEST = (
        "Something is missing in verify password request body."
    )
    OTP_VERIFIED = "OTP verified successfully."
    SOMETHING_MISSING_IN_RESET_PASSWORD_REQUEST = (
        "Something is missing in reset password request body."
    )
    PASSWORD_RESET = "Password reset successfully."
    OLD_PASSWORD_NOT_MATCH = "Old password not match."
    EMAIL_CHANGED = "Email changed successfully."
    INVALID_OTP_TYPE = "Invalid OTP type."
    OTP_NOT_VERIFIED = "OTP not verified."
    EMAIL_ALREADY_EXISTS = "Email already exists."
    NOT_FOUND = "Not found."
    SUCCESS = "Success."

