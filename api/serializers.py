"""
This document contains all the serializers that will be used by the api
"""

from re import U
from django.db import models
from pkg_resources import require
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


class UserUpdateSerializer(serializers.ModelSerializer):
    """
    This is the serializer to update a user
    """

    class Meta:
        """
        The Meta definition for user
        """

        model = User
        fields = ["username", "first_name", "last_name", "password", "birthDate"]
        extra_kwargs = {
            # Avoid return password in the response and Password is not required to update
            "password": {
                "write_only": True,
                "required": False,
            },
            "username": {"required": False},
            "birthDate": {"required": False},
        }

    def update(self, instance, validated_data):
        """
        Update and return an existing User instance, given the validated data.
        """

        instance.username = validated_data.get("username", instance.username)
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        password = validated_data.get("password", None)
        if password is not None:
            instance.set_password(password)
        instance.birthDate = validated_data.get("birthDate", instance.birthDate)
        instance.save()

        return instance


class ChargerTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChargerType
        fields = "__all__"


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
            "iban",
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


class DriverUpdateSerializer(UserUpdateSerializer):
    """
    This is the serializer to update a driver, it inherits from the UserUpdateSerializer
    """

    preference = PreferenceSerializer(required=False)

    class Meta(UserUpdateSerializer.Meta):
        """
        The Meta definition for user
        """

        model = Driver
        fields = UserUpdateSerializer.Meta.fields + [
            "autonomy",
            "chargerTypes",
            "preference",
            "iban",
        ]
        extra_kwargs = UserUpdateSerializer.Meta.extra_kwargs.copy()
        extra_kwargs.update(
            {
                "chargerTypes": {"required": False},
            }
        )

    def update(self, instance, validated_data):
        """
        Update and return an existing Driver instance, given the validated data.
        """
        # Update the user fields
        super().update(instance, validated_data)

        instance.autonomy = validated_data.get("autonomy", instance.autonomy)
        instance.iban = validated_data.get("iban", instance.iban)

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

        instance.save()

        return instance
