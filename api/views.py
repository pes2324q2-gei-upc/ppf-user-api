"""
This file contains all the views to implement the api    
"""

from rest_framework.filters import SearchFilter, OrderingFilter
# from rest_framework.views import APIView
from rest_framework import generics
from ppf.common.models.user import User, Driver
from .serializers import UserSerializer, DriverSerializer, UserRegisterSerializer


class UserList(generics.ListAPIView):
    """
    The class that will generate a list of all the users

    Args:
        generics (ListAPIView): This generates a list of users and pass it as json for the response
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['username']
    order_fields = ['points', 'created_at', 'updated_at']


class DriverList(generics.ListAPIView):
    """
    The class that will generate a list of all the drivers

    Args:
        generics (ListAPIView): This generates a list of users and pass it as json for the response
    """
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['username']
    order_fields = ['driver_points', 'created_at', 'updated_at']


class UserRegister(generics.CreateAPIView):
    """
    The class that will generate a list of all the users

    Args:
        generics (CreateAPIView): This instantiates a user and saves it.
            the response is the instantiated user
    """
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['username']
    order_fields = ['points', 'created_at', 'updated_at']
