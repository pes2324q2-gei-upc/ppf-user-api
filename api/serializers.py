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

    password2 = serializers.CharField(max_length=50, write_only=True, required=False)

    class Meta:
        """
        The Meta definition for user
        """

        model = User
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "points",
            "password",
            "password2",
            "birthDate",
        ]
        extra_kwargs = {
            "points": {"read_only": True},
            "email": {"read_only": True},
            "password": {
                "write_only": True,
                "required": False,
            },
            "password2": {
                "write_only": True,
                "required": False,
            },
            "username": {"required": False},
            "birthDate": {"required": False},
        }

    def validate(self, attrs):
        password = attrs.get("password", None)
        password2 = attrs.get("password2", None)
        if password and not password2:
            raise serializers.ValidationError(
                {"password2": "This field is required when you fill the password."}
            )
        if password2 and not password:
            raise serializers.ValidationError(
                {"password": "This field is required when you fill the password2."}
            )
        if password != password2:
            raise serializers.ValidationError({"password": "Passwords must match."})

        return super().validate(attrs)

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        if password:
            instance.set_password(password)
        return super().update(instance, validated_data)


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
        fields = "__all__"


class PreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Preference
        fields = "__all__"


class DriverSerializer(UserSerializer):
    """
    The Driver serializer class

    Args:
        serializers (ModelSerializer): a serializer model to conveniently manipulate the class
        and create the JSON
    """

    preference = PreferenceSerializer(required=False)

    class Meta:
        """
        The Meta definition for Driver
        """

        model = Driver
        fields = UserSerializer.Meta.fields + [
            "driverPoints",
            "autonomy",
            "chargerTypes",
            "preference",
            "iban",
        ]

        extra_kwargs = UserSerializer.Meta.extra_kwargs.copy()
        extra_kwargs.update(
            {
                "chargerTypes": {"required": False},
                "driverPoints": {"read_only": True},
            }
        )

    def validate(self, attrs):
        return super().validate(attrs)

    def update(self, instance, validated_data):
        chargerTypesData = validated_data.pop("chargerTypes", None)
        if chargerTypesData is not None:
            # Delete all the previous relations
            instance.chargerTypes.clear()
            # Add new relations
            for chargerTypeData in chargerTypesData:
                chargerType = ChargerType.objects.get(chargerType=chargerTypeData)
                instance.chargerTypes.add(chargerType)

        preferenceData = validated_data.pop("preference", None)
        if preferenceData is not None:
            # Update preference fields
            preference = instance.preference
            preference.canNotTravelWithPets = preferenceData.get(
                "canNotTravelWithPets", preference.canNotTravelWithPets
            )
            preference.listenToMusic = preferenceData.get("listenToMusic", preference.listenToMusic)
            preference.noSmoking = preferenceData.get("noSmoking", preference.noSmoking)
            preference.talkTooMuch = preferenceData.get("talkTooMuch", preference.talkTooMuch)
            preference.save()

        return super().update(instance, validated_data)


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
            "iban",
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
