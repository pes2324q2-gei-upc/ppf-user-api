"""
    This module provides an API endpoint for user login.
"""

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from ppf.common.models.user import Token
from .serializers import UserLoginSerializer

# Create your views here.


class LoginAPIView(APIView):
    """
    The class that returns a user token, generating a new one if necessary.

    Args:
        APIView: Base class for handling HTTP requests.
    """

    def post(self, request):
        """
            Handle POST request for user login authentication.

            Parameters:
            - request: HTTP request object containing user login credentials.

            Returns:
            - Response: HTTP response object containing a token or error message.
        """
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            password = serializer.validated_data.get('password')
            user = authenticate(username=username, password=password)

            if user:
                # Find an active token for the user
                token = Token.objects.filter(   # pylint: disable=no-member
                    user=user)
                if token.exists():
                    token = token.delete()

                # Create a new token for the user
                token = Token.objects.create(   # pylint: disable=no-member
                    user=user)
                token.save()

                return Response({'token': token.key})
            # If user not found means that the credentials are invalid or
            # wrong username
            return Response({'error': 'Invalid credentials'},
                            status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_401_UNAUTHORIZED)
