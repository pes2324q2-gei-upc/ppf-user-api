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
        fields = ['id', 'username', 'first_name',
                  'last_name', 'email', 'points']
        extra_kwargs = {
            'points': {'read_only': True},
        }


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
        fields = ['id', 'username', 'first_name',
                  'last_name', 'email', 'driver_points']


class UserRegisterSerializer(serializers.ModelSerializer):
    """
    This is the Serializer for user registration

    Args:
        serializers (ModelSerializer): a serializer model to conveniently manipulate the class
        and create the JSON
    """
    password2 = serializers.CharField(max_length=50, write_only=True)

    class Meta:
        """
        The Meta definition for user
        """
        model = User
        fields = ['username', 'first_name', 'last_name', 'email',
                  'birth_date', 'password', 'password2',]
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError("The passwords do not match")
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')  # Remove password2 from saving
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user


class DriverRegisterSerializer(serializers.ModelSerializer):
    """
    This is the Serializer for user registration

    Args:
        serializers (ModelSerializer): a serializer model to conveniently manipulate the class
        and create the JSON
    """
    password2 = serializers.CharField(max_length=50, write_only=True)

    class Meta:
        """
        The Meta definition for user
        """
        model = Driver
        fields = ['username', 'first_name', 'last_name', 'email',
                  'birth_date', 'password', 'password2', 'dni']
        extra_kwargs = {
            'password': {'write_only': True},
            'driver_points': {'read_only': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError("The passwords do not match")
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')  # Remove password2 from saving
        password = validated_data.pop('password')
        driver = Driver.objects.create_user(**validated_data)
        driver.set_password(password)
        driver.save()
        return driver
