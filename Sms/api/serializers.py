from django.contrib.auth import get_user_model
from rest_framework import serializers

from ..helpers import send_sms
from ..models import *

User = get_user_model()


class SmsGroupSerializer(serializers.Serializer):
    users = serializers.ListField(child=serializers.PrimaryKeyRelatedField(queryset=User.objects.all()))
    message = serializers.CharField()

    def save(self, **kwargs):
        phones = [item.phone for item in self.validated_data.get('users')]
        message = self.validated_data.get('message')

        for phone in phones:
            send_sms(phone, message)

        return True
