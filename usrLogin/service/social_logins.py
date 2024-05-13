from operator import is_
from common.models.user import User
from rest_framework.authtoken.models import Token
from api.serializers import UserRegisterSerializer
from rest_framework import status
from rest_framework.response import Response


def generate_token(user):
    """
    Generate a token for a user.
    """
    # Find an active token for the user
    token = Token.objects.filter(
        user=user)  # pylint: disable=no-member
    if token.exists():
        token = token.delete()

    # Create a new token for the user
    token = Token.objects.create(
        user=user)  # pylint: disable=no-member
    token.save()
    return token


def get_or_create_from_google(data):
    # Check if user exists in the database
    user = User.objects.filter(email=data.get(
        "email"), typeOfLogin="google").first()
    if user:
        # User already exists, return the user
        return user
    else:
        data.update({"typeOfLogin": "google"})
        # User does not exist, create a new user
        serializedUser = UserRegisterSerializer(
            data=data)
        print(serializedUser.is_valid())
        if serializedUser.is_valid():
            user = serializedUser.save()
            return user
        else:
            print(serializedUser.errors)
            return user
        # Return the created user


def ger_or_create_from_facebook(data):
    # Check if user exists in the database
    user = User.objects.filter(email=data.get(
        "email"), typeOfLogin="facebook").first()
    if user:
        # User already exists, return the user
        return user
    else:
        data.update({"typeOfLogin": "facebook"})
        # User does not exist, create a new user
        serializedUser = UserRegisterSerializer(
            data=data)
        print(serializedUser.is_valid())
        if serializedUser.is_valid():
            user = serializedUser.save()
            return user
        else:
            print(serializedUser.errors)
            return user
        # Return the created user
