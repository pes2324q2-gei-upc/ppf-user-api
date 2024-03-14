from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from .serializers import (
    User,
    UserSerializer,
    TokenSerializer,
    UserLoginSerializer
)
from django.utils import timezone
from datetime import timedelta

# Create your views here.


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class TokenList(generics.ListAPIView):
    queryset = Token.objects.all()
    serializer_class = TokenSerializer


class LoginAPIView(APIView):
    """
    The class that returns a user token, generating a new one if necessary.

    Args:
        APIView: Base class for handling HTTP requests.
    """

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            password = serializer.validated_data.get('password')
            user = authenticate(username=username, password=password)

            if user:
                # Find an active token for the user
                try:
                    token = Token.objects.get(user=user)
                    # Check if the token has expired
                    if token.created + timedelta(seconds=30) < timezone.now():
                        # If the token has expired, delete it
                        token.delete()
                        token = None
                except Token.DoesNotExist:
                    token = None

                # If the user does not have an active token, generate a new one
                if not token:
                    token = Token.objects.create(user=user)
                    token.save()

                return Response({'token': token.key})
            # If user not found means that the credentials are invalid or
            # wrong username
            return Response({'error': 'Invalid credentials'},
                            status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_401_UNAUTHORIZED)
