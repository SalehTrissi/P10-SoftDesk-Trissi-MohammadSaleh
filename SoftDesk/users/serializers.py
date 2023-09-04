from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):

    # Define a write-only field for the user's password and age
    password = serializers.CharField(write_only=True)
    age = serializers.IntegerField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'age', 'password')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        # Extract the age from the validated data
        age = validated_data.pop('age')

        # Check if the user is at least 15 years old
        if age > 15:
            # Create a new user object with the provided email
            user = User.objects.create(
                email=validated_data['email'],
            )

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
