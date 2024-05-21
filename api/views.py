"""
This file contains all the views to implement the api    
"""

from re import M
from time import process_time_ns
from urllib import request

from common.models.route import Route
from common.models.user import ChargerType, Driver, Report, User
from common.models.valuation import Valuation
from django.shortcuts import get_object_or_404

# from rest_framework.views import APIView
from rest_framework import generics, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import (
    DriverRegisterSerializer,
    DriverSerializer,
    ReportSerializer,
    UserImageUpdateSerializer,
    UserRegisterSerializer,
    UserSerializer,
    ValuationRegisterSerializer,
    ValuationSerializer,
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


class UserModifyAvatar(generics.UpdateAPIView):
    """
    The class that will modify the avatar of a user

    Args:
        generics (UpdateAPIView): This updates a user and pass it as json for the response
    """

    queryset = User.objects.all()
    serializer_class = UserImageUpdateSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        # Check if the user requesting the action is the same as the user object being retrieved
        if instance.id != request.user.id:
            return Response(
                data={"error": "You can only update your own user account."},
                status=status.HTTP_403_FORBIDDEN,
            )
        return super().update(request, *args, **kwargs)


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
    authentication_classes = [TokenAuthentication]

    def get_permissions(self):
        if self.request.method == "GET":
            self.permission_classes = [AllowAny]
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        # Check if the user requesting the action is the same as the user object being retrieved
        if instance.id != request.user.id:

            return Response(data={"error": "You can only delete your own user account."},
                            status=status.HTTP_403_FORBIDDEN)
        routes = Route.objects.filter(passengers=instance)
        for route in routes:
            route.passengers.remove(instance)

        return super().delete(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        # Check if the user requesting the action is the same as the user object being retrieved
        if instance.id != request.user.id:
            return Response(data={"error": "You can only update your own user account."},
                            status=status.HTTP_403_FORBIDDEN)

        return super().update(request, *args, **kwargs)


class UserRetriever(generics.RetrieveUpdateDestroyAPIView):
    """
    The Retriever for the User class

    Args:
        generics (RetrieveUpdateDestroyAPIView): Concrete view for retrieving,
        updating or deleting a model instance.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    # parser_classes = (FormParser, MultiPartParser)

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        # Check if the user requesting the action is the same as the user object being retrieved
        if instance.id != request.user.id:
            return Response(data={"error": "You can only delete your own user account."},
                            status=status.HTTP_403_FORBIDDEN)
        routes = Route.objects.filter(passengers=instance)
        for route in routes:
            route.passengers.remove(instance)
        return super().delete(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        # Check if the user requesting the action is the same as the user object being retrieved
        if instance.id != request.user.id:
            return Response(
                data={"error": "You can only update your own user account."},
                status=status.HTTP_403_FORBIDDEN,
            )
        return super().update(request, *args, **kwargs)


class ReportListCreate(generics.ListCreateAPIView):
    """
    The class that will generate a list of all the reports and create if needed

    Args:
        generics (ListAPIView): This generates a list of users and pass it as json for the response
    """

    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


class ReportRetriever(generics.RetrieveUpdateDestroyAPIView):
    """
    The Retriever for the Report class

    Args:
        generics (RetrieveUpdateDestroyAPIView): Concrete view for retrieving,
        updating or deleting a model instance.
    """

    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        # Check if the user requesting the action is the same as the user object being retrieved
        if instance.reporter.id != request.user.id:
            return Response(
                data={"error": "You can only delete your own report."},
                status=status.HTTP_403_FORBIDDEN,
            )
        return super().delete(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        # Check if the user requesting the action is the same as the user object being retrieved
        if instance.reporter.id != request.user.id:
            return Response(
                data={"error": "You can only update your own report."},
                status=status.HTTP_403_FORBIDDEN,
            )
        return super().update(request, *args, **kwargs)


class UserIdRetriever(generics.GenericAPIView):
    """
    The class for retrieving the user id from the request

    Args:
        generics (GenericAPIView): Generic view for retrieving the user id.
    """

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        """
        Retrieves the user id from the request.

        Args:
            request (HttpRequest): The request object

        Returns:
            Response: The user id
        """
        user_id = request.user.id
        return Response(data={"user_id": user_id}, status=status.HTTP_200_OK)


class ValuationListCreate(generics.CreateAPIView):
    """
    The class that will generate a list of all the valuations and create if needed

    Args:
        generics (ListAPIView): This generates a list of users and pass it as json for the response
    """

    queryset = Valuation.objects.all()
    serializer_class = ValuationRegisterSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


class MyValuationList(generics.ListAPIView):
    """
    The class that will generate all the valuations of the user logged in

    Args:
        generics (ListAPIView): This generates a list of users and pass it as json for the response
    """

    serializer_class = ValuationSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Valuation.objects.filter(receiver=self.request.user)


class UserValuationList(generics.ListAPIView):
    """
    The class that will generate all the valuations of a user

    Args:
        generics (ListAPIView): This generates a list of users and pass it as json for the response
    """

    serializer_class = ValuationSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = get_object_or_404(User, pk=self.kwargs["user_id"])
        return Valuation.objects.filter(receiver=user)


class DriverToUser(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        try:
            driver = get_object_or_404(Driver, id=request.user.id)
            driver_data = {
                "dni": driver.dni,
                "driverPoints": driver.driverPoints,
                "autonomy": driver.autonomy,
                "chargerTypes": list(driver.chargerTypes.all()),
                "preference": driver.preference,
                "iban": driver.iban,
                "profileImage": driver.profileImage,
                "createdAt": driver.createdAt,
                "birthDate": driver.birthDate,
                "points": driver.points,
            }
            driver.delete()

            # Recreate the user with the same ID (ID is not changed)
            user = User.objects.create(
                id=request.user.id,
                username=request.user.username,
                first_name=request.user.first_name,
                last_name=request.user.last_name,
                email=request.user.email,
                birthDate=driver_data['birthDate'],
                points=driver_data['points'],
                profileImage=driver_data['profileImage'],
                createdAt=driver_data['createdAt'],
            )
            serialaizer = UserSerializer(user)

            return Response(serialaizer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UserToDriver(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        try:
            user = get_object_or_404(User, id=request.user.id)
            data = request.data

            charger_types = data.get('chargerTypes', [])
            charger_types_objs = [ChargerType.objects.get(
                chargerType=ct) for ct in charger_types]

            driver = Driver.objects.create(
                id=request.user.id,
                username=user.username,
                first_name=user.first_name,
                last_name=user.last_name,
                email=user.email,
                birthDate=user.birthDate,
                points=user.points,
                profileImage=user.profileImage,
                createdAt=user.createdAt,
                dni=data['dni'],
                driverPoints=data.get('driverPoints', 0),
                autonomy=data.get('autonomy', 0),
                iban=data.get('iban', '')
            )
            driver.chargerTypes.set(charger_types_objs)
            driver.save()
            print("driver saved")

            return Response({'message': 'You are now a driver.'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
