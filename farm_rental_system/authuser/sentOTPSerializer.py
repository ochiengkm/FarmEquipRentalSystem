from rest_framework import serializers


class sentOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
