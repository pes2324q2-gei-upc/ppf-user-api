"""
This document contains all the serializers that will be used by the api
"""

from django.db import models
from rest_framework import serializers

from common.models.user import Driver, User, ChargerType, Preference


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
        fields = ["id", "username", "first_name", "last_name", "email", "points"]
        extra_kwargs = {
            "points": {"read_only": True},
        }


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
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "birthDate",
            "password",
            "password2",
        ]
        extra_kwargs = {
            "password": {"write_only": True},
            "points": {"write_only": True},
        }

    def validate(self, attrs):
        password = attrs.get("password")
        password2 = attrs.get("password2")
        if password != password2:
            raise serializers.ValidationError("Passwords must match.")

        for field_name, value in attrs.items():
            # Check if the field is not a DateField or DateTimeField
            if not isinstance(value, (models.DateField, models.DateTimeField)):
                if not isinstance(value, str):
                    continue  # Skip validation if value is not a string

                if not value.strip():  # Check if value is a blank string
                    raise serializers.ValidationError(f"{field_name.capitalize()} cannot be blank.")
        return attrs

    def create(self, validated_data):
        validated_data.pop("password2")  # Remove password2 from saving
        password = validated_data.pop("password")
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user


class ChargerTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChargerType
        fields = [
            "chargerType",
        ]


class PreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Preference
        fields = "__all__"


class DriverSerializer(serializers.ModelSerializer):
    """
    The Driver serializer class

    Args:
        serializers (ModelSerializer): a serializer model to conveniently manipulate the class
        and create the JSON
    """

    chargerTypes = ChargerTypeSerializer(many=True)
    preference = PreferenceSerializer()

    class Meta:
        """
        The Meta definition for Driver
        """

        model = Driver
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "driverPoints",
            "chargerTypes",
            "preference",
        ]

        extra_kwargs = {"driverPoints": {"read_only": True}}


class DriverRegisterSerializer(serializers.ModelSerializer):
    """
    This is the Serializer for user registration

    Args:
        serializers (ModelSerializer): a serializer model to conveniently manipulate the class
        and create the JSON
    """

    password2 = serializers.CharField(max_length=50, write_only=True)
    preference = PreferenceSerializer()

    class Meta:
        """
        The Meta definition for user
        """

        model = Driver
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "birthDate",
            "password",
            "password2",
            "dni",
            "autonomy",
            "chargerTypes",
            "preference",
        ]
        extra_kwargs = {
            "password": {"write_only": True, "required": True},
            "driverPoints": {"read_only": True},
        }

    def validate(self, attrs):
        password = attrs.get("password")
        password2 = attrs.get("password2")
        if password != password2:
            raise serializers.ValidationError("Passwords must match.")

        for field_name, value in attrs.items():
            # Check if the field is not a DateField or DateTimeField
            if not isinstance(value, (models.DateField, models.DateTimeField)):
                if not isinstance(value, str):
                    continue  # Skip validation if value is not a string

                if not value.strip():  # Check if value is a blank string
                    raise serializers.ValidationError(f"{field_name.capitalize()} cannot be blank.")
        return attrs

    def create(self, validated_data):
        validated_data.pop("password2")  # Remove password2 from saving
        password = validated_data.pop("password")
        preferenceData = validated_data.pop("preference")
        chargerTypesData = validated_data.pop("chargerTypes", None)

        preference = Preference.objects.create(**preferenceData)

        driver = Driver.objects.create_user(**validated_data, preference=preference)
        driver.set_password(password)
        driver.save()

        if chargerTypesData:
            for chargerTypeData in chargerTypesData:
                chargerType = ChargerType.objects.get(chargerType=chargerTypeData)
                driver.chargerTypes.add(chargerType)

        return driver
