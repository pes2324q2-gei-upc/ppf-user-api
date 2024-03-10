"""
This document contains all the serializers that will be used by the api
"""

from rest_framework import serializers
from ppf.common.models.user import User, Driver


class UserSerializer(serializers.ModelSerializer):
    """
    The User serializer class

    Args:
        serializers (ModelSerializer): a serializer model to conveniently manipulate the class
        and create the JSON
    """
    class Meta:
        """
        The Meta definition for user
        """
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'points']


class DriverSerializer(serializers.ModelSerializer):
    """
    The Driver serializer class

    Args:
        serializers (ModelSerializer): a serializer model to conveniently manipulate the class
        and create the JSON
    """
    class Meta:
        """
        The Meta definition for Driver
        """
        model = Driver
        fields = ['username', 'first_name',
                  'last_name', 'email', 'driver_points']


class UserRegisterSerializer(serializers.ModelSerializer):
    """
    This is the Serializer for user registration

    Args:
        serializers (ModelSerializer): a serializer model to conveniently manipulate the class
        and create the JSON
    """
    password2 = serializers.CharField(max_length=50, write_only=True)
    is_driver = serializers.BooleanField(default=False, write_only=True)

    class Meta:
        """
        The Meta definition for user
        """
        model = User
        fields = ['username', 'first_name', 'last_name', 'email',
                  'birth_date', 'password', 'password2', 'is_driver']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError("The passwords do not match")
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')  # Remove password2 from saving
        is_driver = validated_data.pop('is_driver', False)
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        if is_driver:
            # Logic to mark the user as a driver if needed
            pass  # Add logic here if needed
        return user
