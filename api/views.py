"""
This file contains all the views to implement the api    
"""

from rest_framework.filters import SearchFilter, OrderingFilter
# from rest_framework.views import APIView
from rest_framework import generics
from ppf.common.models.user import User, Driver
from .serializers import UserSerializer, DriverSerializer
from .serializers import UserRegisterSerializer, DriverRegisterSerializer


class UserListCreate(generics.ListCreateAPIView):
    """
    The class that will generate a list of all the users and create if needed

    Args:
        generics (ListAPIView): This generates a list of users and pass it as json for the response
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['username']
    order_fields = ['points', 'created_at', 'updated_at']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return UserRegisterSerializer
        return super().get_serializer_class()


class DriverListCreate(generics.ListCreateAPIView):
    """
    The class that will generate a list of all the drivers and create if needed

    Args:
        generics (ListAPIView): This generates a list of users and pass it as json for the response
    """
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['username']
    order_fields = ['driver_points', 'created_at', 'updated_at']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return DriverRegisterSerializer
        return super().get_serializer_class()
