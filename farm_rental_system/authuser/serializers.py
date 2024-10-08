from rest_framework import serializers
from users.models import CustomUser


class AuthUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['password', 'username']
