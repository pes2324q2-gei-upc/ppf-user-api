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
        The Meta definition for user
        """
        model = Driver
        fields = ['username', 'first_name',
                  'last_name', 'email', 'driver_points']
