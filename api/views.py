"""
This file contains all the views to implement the api    
"""

from rest_framework.filters import SearchFilter, OrderingFilter
# from rest_framework.views import APIView
from rest_framework import generics
from ppf.common.models.user import User, Driver
from .serializers import UserSerializer, DriverSerializer
from .serializers import UserRegisterSerializer, DriverRegisterSerializer


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


class UserRegister(generics.CreateAPIView):
    """
    The class that will handle the creation of the users

    Args:
        generics (CreateAPIView): This instantiates a user and saves it.
            the response is the instantiated user
    """
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer


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


class DriverRegister(generics.CreateAPIView):
    """
    The class that will handle the creation of the Driver

    Args:
        generics (CreateAPIView): This instantiates a driver and saves it.
            the response is the instantiated driver
    """
    queryset = Driver.objects.all
    serializer_class = DriverRegisterSerializer
