
from .serializers import User, UserSerializer
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from ppf.common.models.user import Token
 from .serializers import UserSerializer, TokenSerializer

# Create your views here.


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserRegistrationAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        # Create user
        user = serializer.save()
        password = user.password
        user.set_password(password)
        user.save()

        # Generate and assign token
        token = Token.objects.create(user=user)
        token_serializer = TokenSerializer(instance=token)
        return Response(token_serializer.data, status=status.HTTP_201_CREATED)


class TokenList(generics.ListAPIView):
    queryset = Token.objects.all()
    serializer_class = TokenSerializer
