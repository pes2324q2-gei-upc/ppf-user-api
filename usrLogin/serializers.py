"""
The serializers for the user login
    Returns:
        _type_: _description_
"""

from rest_framework import serializers
from ppf.common.models.user import User, Token


class UserLoginSerializer(serializers.ModelSerializer):
    """
    the serializer for user login
    """
    class Meta:
        """Meta class for user login serializer
        """
        model = User
        fields = ['username', 'password']
        extra_kwargs = {'password': {'write_only': True}}


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
