"""
The serializers for the user login
    Returns:
        _type_: _description_
"""

from rest_framework import serializers
from ppf.common.models.user import User, Token


class UserLoginSerializer(serializers.Serializer):
    """
    Serializer for handling user login data.

    Args:
        Serializer: Base class for serializers in Django REST Framework.
    """
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(max_length=128, write_only=True)


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for user login

    Args:
        serializers (ModelSerializer): basic serializer model

    Returns:
        _type_: _description_
    """
    class Meta:
        """meta class for user serializer
        """
        model = User
        fields = ['username', 'password']  # Add other fields as needed
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class TokenSerializer(serializers.ModelSerializer):
    """
    serializer class for the tokens
    """
    class Meta:
        """
        meta class for the tokens
        """
        model = Token
        fields = '__all__'
