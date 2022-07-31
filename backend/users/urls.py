from django.urls import path
from users.views import (RegistrationView,
                         SignInView
                         )

urlpatterns = [
    path("registration/", RegistrationView.as_view(), name="register-new-user"),
    path("sign-in/", SignInView.as_view(), name="sign-in-user"),
]
