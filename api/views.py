"""
This file contains all the views to implement the api    
"""

from common.models.user import Driver, User

# from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.filters import OrderingFilter, SearchFilter

from .serializers import (
    DriverRegisterSerializer,
    DriverSerializer,
    UserRegisterSerializer,
    UserSerializer,
    UserUpdateSerializer,
    DriverUpdateSerializer,
)


class UserListCreate(generics.ListCreateAPIView):
    """
    The class that will generate a list of all the users and create if needed

    Args:
        generics (ListAPIView): This generates a list of users and pass it as json for the response
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["username"]
    order_fields = ["points", "createdAt", "updatedAt"]

    def get_serializer_class(self):
        if self.request.method == "POST":
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
    search_fields = ["username"]
    order_fields = ["driverPoints", "createdAt", "updatedAt"]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return DriverRegisterSerializer
        return super().get_serializer_class()


class DriverRetriever(generics.RetrieveUpdateDestroyAPIView):
    """
    The Retriever for the Driver class

    Args:
        generics (RetrieveUpdateDestroyAPIView): Concrete view for retrieving,
        updating or deleting a model instance.
    """

    queryset = Driver.objects.all()
    serializer_class = DriverSerializer

    def get_serializer_class(self):
        if self.request.method == "PUT" or self.request.method == "PATCH":
            return DriverUpdateSerializer
        return super().get_serializer_class()


class UserRetriever(generics.RetrieveUpdateDestroyAPIView):
    """

    The Retriever for the User class

    Args:
        generics (RetrieveUpdateDestroyAPIView): Concrete view for retrieving,
        updating or deleting a model instance.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_serializer_class(self):
        if self.request.method == "PUT" or self.request.method == "PATCH":
            return UserUpdateSerializer
        return super().get_serializer_class()
