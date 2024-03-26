"""
This file is used to serialize the data that is sent to the server.
"""

from rest_framework import serializers


class EmailSerializer(serializers.Serializer):
    """
    Serializer to validate the data sent to the server

    Args:
        Serializer: Base class for serializers in Django REST Framework.
    """

    inquiry = serializers.CharField(max_length=120)
    message = serializers.CharField()
    email = serializers.ListField(child=serializers.EmailField())

    def create(self, validated_data):
        return

    def update(self, instance, validated_data):
        return
