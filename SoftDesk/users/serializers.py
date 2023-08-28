from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'name', 'email', 'age', 'password')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User.objects.create(
            name=validated_data['name'],
            email=validated_data['email'],
            age=validated_data['age'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    def validate_email(self, value):
        """
        Custom validation for the email field.
        Checks if the provided email address is already in use by another user.
        """
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "This email is already registered. Please use a different email."
            )
        return value

    def validate_password(self, value):
        """
        Custom validation for the password field.
        You can add your own password complexity rules here.
        In this example, it checks that the password is at least 8 characters long.
        """
        if len(value) < 8:
            raise serializers.ValidationError(
                "Password must be at least 8 characters long."
            )
        return value
