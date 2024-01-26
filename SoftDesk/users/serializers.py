from .models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    # Define write-only fields for password, age, and consent
    password = serializers.CharField(write_only=True)
    age = serializers.IntegerField(write_only=True)
    has_consent = serializers.BooleanField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email',
                  'age', 'password', 'has_consent')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        # Extract the age from the validated data
        age = validated_data.pop('age')

        # Check if the user is at least 15 years old
        if age >= 15:
            # Create a new user object with the provided data
            user = super().create(validated_data)

            # Set the user's password
            user.set_password(validated_data['password'])

            # Store the user's age in the model
            user.age = age

            # Save the user object to the database
            user.save()
            return user
        else:
            # Raise a validation error if the user is not old enough
            raise serializers.ValidationError(
                "You must be at least 15 years old to register."
            )

    def validate_email(self, value):
        # Custom validation for the email field
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "This email is already registered. Please use a different email."
            )
        return value

    def validate_password(self, value):
        # Custom validation for the password field
        if len(value) < 8:
            raise serializers.ValidationError(
                "Password must be at least 8 characters long."
            )
        return value
