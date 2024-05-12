from common.models.user import User
from rest_framework.authtoken.models import Token


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
        # User does not exist, create a new user
        user = User()
        user.email = data.get("email")
        user.username = data.get("email").split("@")[0]
        user.birthDate = data.get("birthDate")
        user.password = data.get("")
        user.typeOfLogin = "google"
        user.save()
        return user

    # Return the created user
