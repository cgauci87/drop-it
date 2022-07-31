import logging
from django.conf import settings
from rest_framework import serializers

from utils.mock_responses import ResponseMessages
from users.models import (
    User
)
from datetime import datetime

logger = logging.getLogger(settings.LOGGER_NAME_PREFIX + __name__)



class RegistrationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, attrs):
        if attrs["email"]:
            if User.objects.filter(email=attrs["email"]).exists():
                logger.error(f"Email already exists: {attrs['email']}")
                raise serializers.ValidationError(
                    ResponseMessages.EMAIL_ALREADY_EXISTS.value
                )
        
        return attrs

    def create(self, validated_data):
        # generate random username
        username = validated_data["first_name"] + validated_data["last_name"] + str(datetime.now().timestamp()).split(".")[1]
        validated_data["username"] = username
        user = User.objects.create_user(**validated_data)
        return user
