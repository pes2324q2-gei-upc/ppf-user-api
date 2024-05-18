"""
This file contains all the views to implement the api    
"""

from api.notifications.push_controller import PushController
from common.models.route import Route
from common.models.user import Driver, Report, User
from common.models.valuation import Valuation
from django.shortcuts import get_object_or_404
from firebase_admin.exceptions import FirebaseError

# from rest_framework.views import APIView
from rest_framework import generics, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

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

pushController = PushController()


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
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        # Check if the user requesting the action is the same as the user object being retrieved
        if instance.id != request.user.id:
            return Response(
                data={"error": "You can only delete your own user account."},
                status=status.HTTP_403_FORBIDDEN,
            )

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
            return Response(
                data={"error": "You can only delete your own user account."},
                status=status.HTTP_403_FORBIDDEN,
            )
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


class RegisterFCMToken(generics.CreateAPIView):
    """
    The class that will register the FCM token of the user

    Args:
        CreateAPIView: This creates a new FCM token and pass it as json for the response
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        # Retrieve the user
        user = request.user
        # Retrieve the fcm token
        try:
            pushController.addToken(user, request.data["token"])
        except FirebaseError as e:
            return Response(data={"error": "Error creating the FCM token"}, status=e.code)

        return Response(status=status.HTTP_201_CREATED)


class SendFCMNotification(generics.CreateAPIView):
    """
    The class that will send a FCM notification to a user

    Args:
        CreateAPIView: This creates a new FCM notification and pass it as json for the response
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def validate(self, request):
        if request.data["title"] is None or request.data["body"] is None:
            return Response(
                data={"error": "Title and body are required"}, status=status.HTTP_400_BAD_REQUEST
            )
        if request.data["title"] == "" or request.data["body"] == "":
            return Response(
                data={"error": "Title and body cannot be empty"}, status=status.HTTP_400_BAD_REQUEST
            )
        return None

    def create(self, request, *args, **kwargs):
        # Retrieve the user
        user = request.user

        # Retrieve the fcm token
        validation = self.validate(request)
        if validation is not None:
            return validation

        # Check if user has a device token
        token = pushController.token(user)
        if token is None:
            return Response(
                data={"error": "User does not have a device token"},
                status=status.HTTP_403_FORBIDDEN,
            )

        try:
            pushController.notifyTo(user, request.data["title"], request.data["body"])
        except FirebaseError as e:
            return Response(data={"error": "Error sending the FCM notification"}, status=e.code)
        return Response(status=status.HTTP_201_CREATED)
