from django.db import models
from baselayer.basemodels import LogsMixin
from django.contrib.auth.models import AbstractUser
from baselayer.baseauthentication import generate_access_token

#Choice classes
class UserTypeChoices(models.TextChoices):
    ADMIN = 1, "Admin"
    MODIRATOR = 2, "Modirator"
    USER = 3, "User"

# Create your models here.

class User(LogsMixin, AbstractUser):
    user_type = models.CharField(choices=UserTypeChoices.choices, null=True, blank=True, max_length=25, default=UserTypeChoices.USER)
    location = models.CharField(max_length=100, null=True, blank=True)
    skill_level = models.CharField(max_length=100, null=True, blank=True)

    def get_access_token(self):
        return generate_access_token(self)