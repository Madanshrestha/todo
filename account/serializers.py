
from django.contrib.auth import get_user_model

from rest_framework import serializers

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True, allow_blank=False, )

    class Meta:
        model = User
        fields = ['url', 'username', 'email']