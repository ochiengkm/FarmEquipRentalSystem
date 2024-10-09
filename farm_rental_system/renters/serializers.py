from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from utils.Helpers import Helpers

from renters.models import Renters


class RentersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Renters
        fields = ['first_name', 'last_name', 'email', 'phone_number']

    def create(self, validated_data):
        helpers = Helpers()  # Instantiate the Helpers class

        # Extract the phone number to use as the password
        phone_number = validated_data.get('phone_number',)
        if not phone_number:
            raise serializers.ValidationError("Phone number is required to create a user.")

        # Use the phone number as the password
        plain_password = phone_number

        # Print the plain password for debugging
        print(f"Generated password: {plain_password}")

        # Generate username by concatenating first name and last name
        first_name = validated_data.get('first_name', '').capitalize()
        last_name = validated_data.get('last_name', '').capitalize()
        username = f"{first_name}{last_name}"

        # Ensure username is unique
        if Renters.objects.filter(username=username).exists():
            count = Renters.objects.filter(username__startswith=username).count()
            username = f"{username}{count + 1}"

        # Set the generated username in the validated_data
        validated_data['username'] = username

        # Hash the plain password (phone number)
        validated_data['password'] = make_password(plain_password)

        # Create the user with the hashed password and generated username
        user = super(RentersSerializer, self).create(validated_data)

        # Extract the email to send the generated password
        email = validated_data.get('email')
        if email:
            helpers.send_generated_password(first_name, username, plain_password, email)

        return user